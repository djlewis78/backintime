# Back In Time
# Copyright (C) 2008-2015 Oprea Dan, Bart de Koning, Richard Bailey, Germar Reitze
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public Licensealong
# with this program; if not, write to the Free Software Foundation,Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import unittest
import subprocess
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common/"))

from applicationinstance import ApplicationInstance


class TestApplicationInstance(unittest.TestCase):
    def setUp(self):
        self.t = 1

    def test_existing_process_with_correct_procname(self):
        """
        Test the check function with an existing process with correct process
        name
        """
        #              GIVE               #
        # Creation of thread to get a pid
        temp_file = 'temp.txt'
        with open(temp_file, 'wt') as output:
            subproc = subprocess.Popen("top", stdout=output)
            pid = subproc.pid
        # Get the process name
        with open('/proc/%s/cmdline' % pid, 'r') as file:
            procname = file.read().strip('\n')

        # create file with pid and process name
        file_name = "file_with_pid"
        with open(file_name, "wt") as file_with_pid:
            file_with_pid.write(str(pid) + "\n")
            file_with_pid.write(procname)

        #               WHEN             #
        inst = ApplicationInstance(os.path.abspath(file_name), False)
        result = inst.check()

        #               THEN             #
        # Clean files and process
        subproc.kill()
        os.remove(temp_file)
        os.remove(file_name)
        # Execute test
        self.assertFalse(result)

    def test_killing_existing_process(self):
        """
        Test the check function when it kills a instance of existing process
        """
        #              GIVE               #
        # Creation of thread to get a pid
        temp_file = 'temp.txt'
        with open(temp_file, 'wt') as output:
            subproc = subprocess.Popen("top", stdout=output)
            pid = subproc.pid
        # Get the process name
        with open('/proc/%s/cmdline' % pid, 'r') as file:
            procname = file.read().strip('\n')

        # create file with pid and process name
        file_name = "file_with_pid"
        with open(file_name, "wt") as file_with_pid:
            file_with_pid.write(str(pid) + "\n")
            # Necessary, because os.kill can't kill Popen Process
            file_with_pid.write(procname + "DELETE")

        #               WHEN             #
        inst = ApplicationInstance(os.path.abspath(file_name), False)
        result = inst.check()

        #               THEN             #
        # Clean files and process
        subproc.kill()
        os.remove(temp_file)
        os.remove(file_name)

        # Execute test
        self.assertTrue(result)

    def test_non_existing_process(self):
        """ Test the check function with a non existing process """
        #              GIVE               #
        # create file with pid and process name
        file_name = "file_with_pid"
        with open(file_name, "wt") as file_with_pid:
            file_with_pid.write("987654321\n")
            file_with_pid.write("FAKE_PROCNAME")

        #               WHEN             #
        inst = ApplicationInstance(os.path.abspath(file_name), False)
        result = inst.check()

        #               THEN             #
        # Clean files and process
        os.remove(file_name)

        # Execute test
        self.assertTrue(result)


# Execute tests if this programm is call with python TestApplicationInstance.py
if __name__ == '__main__':
    unittest.main()
