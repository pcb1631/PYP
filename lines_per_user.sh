#!/bin/bash

# Script to get lines added and deleted per user, excluding booking.json

echo "Lines added/deleted per user (excluding booking.json):"
echo "=================================================="
echo

# Get git log with line statistics, exclude booking.json, and aggregate by author
git log --numstat --pretty=format:"%an" --no-merges | \
awk '
BEGIN {
    print "Author                | Lines Added | Lines Deleted | Net Change"
    print "---------------------|-------------|---------------|-----------"
}
/^[a-zA-Z]/ {
    author = $0
    next
}
/^[0-9]/ {
    if ($3 !~ /booking\.json/) {
        added[author] += $1
        deleted[author] += $2
        net[author] += ($1 - $2)
    }
}
END {
    for (a in added) {
        printf "%-20s | %11d | %13d | %11d\n", a, added[a], deleted[a], net[a]
    }
}
' | sort -k4 -nr

echo
echo "Total lines per user (excluding booking.json):"
echo "=============================================="
echo

# Alternative view showing total contribution
git log --numstat --pretty=format:"%an" --no-merges | \
awk '
/^[a-zA-Z]/ {
    author = $0
    next
}
/^[0-9]/ {
    if ($3 !~ /booking\.json/) {
        total[author] += $1 + $2
    }
}
END {
    for (a in total) {
        printf "%-20s | %11d total lines\n", a, total[a]
    }
}
' | sort -k2 -nr
