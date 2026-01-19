# Copyright 2016-2023 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause
import reframe as rfm
import reframe.utility.sanity as sn
import os


@rfm.simple_test
class stream_build_test(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['joey:login']
        self.valid_prog_environs = ['PrgEnv-gnu']
        self.build_system = 'SingleSource'
        self.sourcepath = 'stream.c'
        self.executable = './stream.x'

        if self.benchmark_mode:
            self.reference = {
                'joey:login': {
                    'copy_bw': (25000, [None, -0.60, -0.20, 0], [-0.60, -0.20, 0, None], 'MB/s'),
                    'triad_bw': (15000, [None, -0.60, -0.20, 0], [-0.60, -0.20, 0, None], 'MB/s'),
                }
            }
        else:
            self.reference = {
                'joey:login': {
                    'copy_bw': (25000, -0.2, 0.2, 'MB/s'),
                    'triad_bw': (15000, -0.2, 0.2, 'MB/s'),
                }
            }

    @run_before('compile')
    def prepare_build(self):
        self.build_system.cflags = ['-O3', '-fopenmp']

    @sanity_function
    def validate(self):
        return sn.assert_found(r'Solution Validates', self.stdout)

    @performance_function('MB/s')
    def copy_bw(self):
        return sn.extractsingle(r'Copy:\s+(\S+)', self.stdout, 1, float)

    @performance_function('MB/s')
    def triad_bw(self):
        return sn.extractsingle(r'Triad:\s+(\S+)', self.stdout, 1, float)
