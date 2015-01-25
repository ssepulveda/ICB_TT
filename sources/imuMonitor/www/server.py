import sys

from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession

from mainProcess import MainProcess

## IMU class to access data
#
# Defines callbacks and register events for WAMP server
# @param ApplicationSession WAMP instance
class Imu(ApplicationSession):
	## onJoin event (server connected)
	#
	# Starts the MainProcess when server starts, initing the communication
	# thread with the IMU
	# @param self The object pointer.
	# @param details WAMP data
    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self)
        print("Server connected")

        # start imu server
        self.app = MainProcess()

	## onLeave event (server disconnected)
	#
	# Stops the MainProcess when server stops.
	# @param self The object pointer.
	# @param details WAMP data
    @inlineCallbacks
    def onLeave(self, details):
        print("Server disconnected")
        if self.app.is_alive():
            self.app.join()

	## test function
	#
	# Checks the WAMP and WebSocket working with a defined Value
	# @param self The object pointer.
	# @param arg Expected data from the WebSocket
	# @return Server status
    @wamp.register(u'com.example.imu.test')
    def test(self, arg=None):
        return str("Servidor operativo")

	## Detects the number of connected IMUs
	#
	# @param self The object pointer.
	# @param arg Expected data from the WebSocket
	# @return number of IMUs detected
    @wamp.register(u'com.example.imu.detect')
    def detectImu(self, arg=None):
        resp = self.app.detectImu()
        countImu = 0
        if not resp:
            return str("No imu detected !")
        else:
            for n, r in enumerate(resp):
                if r is True:
                    countImu += 1
            return str(countImu)

	## Sets filename for the CSV export
	#
	# @param self The object pointer.
	# @param arg file name
    @wamp.register(u'com.example.imu.filename')
    def setFileName(self, arg):
        print arg
        self.app.setFileName(str(arg))

	## Gets filename of the current CSV export
	#
	# @param self The object pointer.
	# @param arg Expected data from the WebSocket
	# @return file name
    def getFileName(self, arg=None):
        return self.app.getFileName()

	## Starts adquisition
	#
	# Inits data adquisition from the detected IMUs in another thread
	# @param self The object pointer.
	# @param arg Expected data from the WebSocket
    @wamp.register(u'com.example.imu.startimu')
    def startImu(self, arg=None):
        print("Start")
        self.app.start()

	## Stops adquisition
	#
	# Stops data adquisition and the corresponding thread
	# @param self The object pointer.
	# @param arg Expected data from the WebSocket
    @wamp.register(u'com.example.imu.stopimu')
    def stoptImu(self, arg=None):
        print("Stop")
        self.app.stop()
        self.app.join(1)

	## Get data
	#
	# Gets the current data from the current enabled sensor
	# @param self The object pointer.
	# @param arg Expected data from the WebSocket
	# @return sensor data
    @wamp.register(u'com.example.imu.getdata')
    def getImuData(self, arg=None):
        data = self.app.getData()
        print data
        return data


if __name__ == '__main__':
    import sys
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")
    parser.add_argument("--web", type=int, default=8080,
                        help='Web port to use for embedded Web server. Use 0 to disable.')
    parser.add_argument("--router", type=str, default=None,
                        help='If given, connect to this WAMP router. Else run an embedded router on 9000.')
    args = parser.parse_args()

    if args.debug:
        from twisted.python import log
        log.startLogging(sys.stdout)

    # import Twisted reactor
    from twisted.internet import reactor

    # create embedded web server for static file
    if args.web:
        from twisted.web.server import Site
        from twisted.web.static import File

        reactor.listenTCP(args.web, Site(File(".")))


    # run WAMP application component
    from autobahn.twisted.wamp import ApplicationRunner
    router = args.router or 'ws://localhost:9000'
    runner = ApplicationRunner(router, u"realm1", standalone=not args.router,
                               debug=False,  # low-level logging
                               debug_wamp=args.debug,  # WAMP level logging
                               debug_app=args.debug)  # app-level logging

    # start the component and the Twisted reactor ..
    runner.run(Imu)
