"""
Unittests for functions from the helpers module.

"""

import os
import types
import tempfile
import shutil

import pytest

from pyxmaxlibs.helpers import print_msg_exit
from pyxmaxlibs.helpers import get_files
from pyxmaxlibs.helpers import ask_question
from pyxmaxlibs.helpers import get_random_string


def test_print_msg_exit(capsys):
    with pytest.raises(SystemExit):
        print_msg_exit()
        out, err = capsys.readouterr()
        assert out == ""
        msg = "My exit msg"
        print_msg_exit(msg=msg)
        out, err = capsys.readouterr()
        assert out == msg + '\n'


def _create_tmp_dir(path="/tmp", num_sub_dirs=0, num_files=0):
    """
    Creates temporary directory in path.
    Creates num_files files in the new directory.
    Creates num_sub_dirs in the directory each of which will have
        num_files files.
    Returns root directory and a list of newly created files, absolute paths.

    """
    def create_file(path):
        fd, abspath = tempfile.mkstemp(dir=path)
        return abspath

    root = tempfile.mkdtemp(dir=path)
    lst = []
    # create files in the root dir of the temp dir 
    for i in range(num_files):
        lst.append(create_file(root))
    # create subdirectories
    dirs = []
    for i in range(num_sub_dirs):
        subdir = tempfile.mkdtemp(dir=root)
        dirs.append(subdir)
    # create files in the subdirectories
    for d in dirs:
        for i in range(num_files):
            lst.append(create_file(d))
    return root, lst



class TestGetFiles(object):
    """
    Test get_files function.
    Handy to have those in a class to control setup and teardown
    sequence.

    """

    def setup_method(self, method):
        pass
        # need to control the call of _create_tmp_dir(), for each method
        # it will be different, do manually in the test methods 


    def teardown_method(self, method):
        print("Teardown TestGetFiles")
        print("Root: %s, exists: %s" % (self.root, os.path.exists(self.root)))
        shutil.rmtree(self.root)
        print("Root: %s, exists: %s" % (self.root, os.path.exists(self.root)))


    def test_get_files_empty(self):
        lst_files = get_files()
        assert isinstance(lst_files, types.ListType)
        self.root, self.temp_files = _create_tmp_dir()
        lst_files = get_files(path=self.root)
        assert lst_files == []
    
    
    def test_get_files_populated(self):
        self.root, temp_files = _create_tmp_dir(num_files=4)
        #print self.temp_files
        lst_files = get_files(path=self.root)
        assert len(lst_files) == 4
        txtfile = os.path.join(self.root, "test.txt")
        open(txtfile, 'w').close()
        lst_files = get_files(path=self.root, file_mask="*.txt")
        assert len(lst_files) == 1
        assert lst_files[0] == txtfile

    
    def test_get_files_populated_recursive(self):
        self.root, temp_files = _create_tmp_dir(num_files=2, num_sub_dirs=3)
        lst_files = get_files(path=self.root, recursive=True)
        # 2 files in the root plus 3 dirs with 2 files = 8 files total
        assert len(lst_files) == 8
        assert sorted(temp_files) == sorted(lst_files)


    def test_get_files_multiple_masks(self):
        self.root, temp_files = _create_tmp_dir(num_files=2, num_sub_dirs=3)
        # 8 files in total, rename
        for i in range(4):
            new_name = temp_files[i] + ".txt"
            os.rename(temp_files[i], new_name)
            temp_files[i] = new_name
        for i in range(4, len(temp_files)):
            new_name = temp_files[i] + ".pas"
            os.rename(temp_files[i], new_name)
            temp_files[i] = new_name
        # wrong mask specified
        l = get_files(path=self.root, file_mask=".txt", recursive=True)
        assert len(l) == 0
        l = get_files(path=self.root, file_mask="*.txt", recursive=True)
        assert len(l) == 4
        l = get_files(path=self.root,
                      file_mask=["*.txt", "*.pas"],
                      recursive=True)
        # everything 
        assert len(l) == 8
        assert sorted(temp_files) == sorted(l)
        l = get_files(path=self.root,
                      file_mask=["*.txt", "*.doc"],
                      recursive=True)
        assert len(l) == 4



def test_ask_question():
    pytest.raises(ValueError, ask_question, "Message:", answers="a/b/")
    pytest.raises(ValueError, ask_question, "Message:", answers="[a]")
    pytest.raises(ValueError, ask_question, "Message:", answers="[a/b/c]",
                                             default="d")
    # simulate input on stdin
    import pyxmaxlibs.helpers
    # redefine raw_input() function for the module
    pyxmaxlibs.helpers.raw_input = lambda: "up"
    answer = ask_question("Message:", answers="[Down/Up]", default="up")
    assert answer == "up"
    
    pyxmaxlibs.helpers.raw_input = lambda: "u"
    answer = ask_question("Message:", answers="[Down/Up]", default="up")
    assert answer == "up"

    pyxmaxlibs.helpers.raw_input = lambda: "d"
    answer = ask_question("Message:", answers="[Down/Up]", default="up")
    assert answer == "down"

    pyxmaxlibs.helpers.raw_input = lambda: ''
    answer = ask_question("Message:", answers="[Down/Up]", default="up")
    assert answer == "up"


def test_get_random_string():
    pytest.raises(ValueError, get_random_string, 'a', 'C', 10)
    pytest.raises(ValueError, get_random_string, 'a', 'C', 0)
    s = get_random_string('C', 'a', 10)
    assert len(s) == 10
    s = get_random_string('a', 'b', 5)
    assert s == "aaaaa" # 5x 'a'
