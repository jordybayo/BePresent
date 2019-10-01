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
"""A XML RPC server .
    USAGE :
        module not in usage but # TODO in the future for structure data type tranfer
"""

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def main():
    # Create server
    with SimpleXMLRPCServer(('localhost', 8000),requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        # Register pow() function; this will use the value of
        # pow.__name__ as the name, which is just 'pow'.
        server.register_function(pow)

        # Register a function under a different name
        def adder_function(x, y):
            return x + y
        server.register_function(adder_function, 'add')

        # Register an instance; all the methods of the instance are
        # published as XML-RPC methods (in this case, just 'mul').
        class MyFuncs:
            def mul(self, x, y):
                return x * y

        server.register_instance(MyFuncs())

        # Run the server's main loop
        server.serve_forever()



if __name__ == '__main__':
    main()