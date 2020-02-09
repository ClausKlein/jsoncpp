#!/usr/bin/env python3 -tt

import sys
import os
import time
import subprocess


def gettime(command):
    if command is None:
        return 0.0
    print('Running command:', command)
    starttime = time.time()
    subprocess.check_call(command, shell=True, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    endtime = time.time()
    return endtime - starttime


def measure():
    measurements = [
        ['cmake-make', 'rm -rf build-cmake && mkdir -p build-cmake && cd build-cmake && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release ..',
            'cd build-cmake && make -j 2', 'cd build-cmake && make -j 2 clean'],
        ['cmake-ninja', 'rm -rf build-cmake-ninja && mkdir -p build-cmake-ninja && cd build-cmake-ninja && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release -G Ninja ..',
            'cd build-cmake-ninja && ninja -j 2', 'cd build-cmake-ninja && ninja -j 2 clean'],
        ['meson', 'rm -rf build-meson && mkdir -p build-meson && CC=\'ccache g++\' meson build-meson',
            'ninja -C build-meson -j 2', 'ninja -C build-meson -j 2 clean'],
    ]
    results = []
    for m in measurements:
        cur = []
        results.append(cur)
        cur.append(m[0])
        conf = m[1]
        make = m[2]
        clean = m[3]
        cur.append(gettime(conf))
        cur.append(gettime(make))
        cur.append(gettime(make))
        cur.append(gettime(clean))
        cur.append(gettime(make))
    return results


def print_times(times):
    for t in times:
        print(t[0])
        print(" %.3f gen" % t[1])
        print(" %.3f build" % t[2])
        print(" %.3f empty build" % t[3])
        print(" %.3f clean" % t[4])
        print(" %.3f rebuild" % t[5])
        overall = t[1] + t[2] + t[3] + t[4] + t[5]
        print(" %.3f overall" % overall)


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print(sys.argv[0], '<output dir>')
    # os.chdir(sys.argv[1])
    print_times(measure())
