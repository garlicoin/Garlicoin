// Copyright (c) 2011-2017 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.
//
#include <timedata.h>
#include <test/test_bitcoin.h>

#include <limits>

#include <boost/test/unit_test.hpp>

BOOST_FIXTURE_TEST_SUITE(timedata_tests, BasicTestingSetup)

BOOST_AUTO_TEST_CASE(util_MedianFilter)
{
    CMedianFilter<int> filter(5, 15);

    BOOST_CHECK_EQUAL(filter.median(), 15);

    filter.input(20); // [15 20]
    BOOST_CHECK_EQUAL(filter.median(), 17);

    filter.input(30); // [15 20 30]
    BOOST_CHECK_EQUAL(filter.median(), 20);

    filter.input(3); // [3 15 20 30]
    BOOST_CHECK_EQUAL(filter.median(), 17);

    filter.input(7); // [3 7 15 20 30]
    BOOST_CHECK_EQUAL(filter.median(), 15);

    filter.input(18); // [3 7 18 20 30]
    BOOST_CHECK_EQUAL(filter.median(), 18);

    filter.input(0); // [0 3 7 18 30]
    BOOST_CHECK_EQUAL(filter.median(), 7);
}

BOOST_AUTO_TEST_CASE(peer_time_offset_bounds)
{
    const int64_t min_time = std::numeric_limits<int64_t>::min();
    const int64_t max_time = std::numeric_limits<int64_t>::max();
    int64_t offset = 123;

    BOOST_CHECK(ComputePeerTimeOffset(1700000060, 1700000000, offset));
    BOOST_CHECK_EQUAL(offset, 60);
    BOOST_CHECK(ComputePeerTimeOffset(1699999940, 1700000000, offset));
    BOOST_CHECK_EQUAL(offset, -60);

    // A failed calculation must not overwrite the previous offset.
    BOOST_CHECK(!ComputePeerTimeOffset(min_time, 1, offset));
    BOOST_CHECK_EQUAL(offset, -60);
    BOOST_CHECK(!ComputePeerTimeOffset(max_time, -1, offset));
    BOOST_CHECK_EQUAL(offset, -60);
    BOOST_CHECK(!ComputePeerTimeOffset(0, min_time, offset));

    // Boundary differences that fit into int64_t are still accepted.
    BOOST_CHECK(ComputePeerTimeOffset(min_time + 1, 1, offset));
    BOOST_CHECK_EQUAL(offset, min_time);
    BOOST_CHECK(ComputePeerTimeOffset(max_time - 1, -1, offset));
    BOOST_CHECK_EQUAL(offset, max_time);
    BOOST_CHECK(ComputePeerTimeOffset(min_time, 0, offset));
    BOOST_CHECK_EQUAL(offset, min_time);
    BOOST_CHECK(ComputePeerTimeOffset(max_time, 0, offset));
    BOOST_CHECK_EQUAL(offset, max_time);
    BOOST_CHECK(ComputePeerTimeOffset(0, max_time, offset));
    BOOST_CHECK_EQUAL(offset, -max_time);
}

BOOST_AUTO_TEST_SUITE_END()
