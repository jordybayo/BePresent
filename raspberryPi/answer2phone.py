# Copyright 2019 The Bayo. All Rights Reserved.
#
# Licensed under the Bayobrain License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.bayobrain.org/licenses/LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A Face recognition Module based on Opencv .

    IMPORTS :
        -   from controler.detector import verifier

    CLASS :
        -   FaceDetection

        - METHODS :

             - __init__(self)

             - start_detection(self)


    MATERIALS REQUIREMENTS :

        -   Required Camera plugin and permission to use.

    USAGE : This file is not usable right now and don't have an importance
"""

from controler.detector import verifier


class FaceDetection:

    def __init__(self):
        pass

    def start_detection(self):
        verifier()



def main():
    r_t = FaceDetection()
    r_t.start_detection()


if __name__ == '__main__':
    main()
