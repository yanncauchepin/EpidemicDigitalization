import os
import sys
from Modules.Place import initDataPlace
from Modules.Script import HandlerScripts
from Modules.Tools.Style import color

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

SUMOFILES = "Modules/SumoMobility/SumoFiles"
OUTPUT = "Modules/SumoMobility/Report"

CONFIG_NETWORK = "network.netcfg"
NETWORK = "network.net.xml"

CONFIG_POLYGON = "polygon.polycfg"
POLYGON_TYPES = "polygon.types.xml"
POLYGONS = "polygons.poly.xml"

VIEW = "spreading.view.xml"

PT_STOPS = "pt.stops.xml"
PT_STOPINFOS = "pt.stopinfos.xml"
PT_LINES = "pt.lines.xml"
PT_TRIPS = "pt.trips.xml"
PT_ROUTES = "pt.routes.xml"
PT_VEHICLES = "pt.vehicules.xml"

PEOPLE_TRIPS = "people.trips.xml"
PEOPLE_TEMP_ROUTES = "people.temp.routes.xml"
PEOPLE_TEMP_ALT_ROUTES = "people.temp.alt.routes.xml"
PEOPLE_ROUTES = "people.routes.xml"
CONFIG_DUAROUTER = "people.duaconfig"

OUTPUT_TRIP = "tripinfo.xml"
OUTPUT_TIMESTATE = "timestate.xml"

CONFIG_SUMO = "spreading.sumocfg"

class HandlerSumo():

    def __init__(self, path, osm) :

        self.__path=str(path)
        self.__osm=str(osm)

    def getPath(self) :
        return self.__path

    def getOsm(self) :
        return self.__osm

    def __setDaySumoConfig (self, day, **kwargs) :

        path = self.getPath()
        file = kwargs.get("config_sumo", f"{SUMOFILES}/{day}.{CONFIG_SUMO}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        polygons = kwargs.get("polygons", f"{SUMOFILES}/{POLYGONS}")
        view = kwargs.get("view", f"{SUMOFILES}/{VIEW}")
        pt_stops = kwargs.get("pt_stops", f"{SUMOFILES}/{PT_STOPS}")
        people_routes = kwargs.get("people_routes", f"{SUMOFILES}/{day}.{PEOPLE_ROUTES}")
        pt_routes = kwargs.get("pt_routes", f"{SUMOFILES}/{PT_ROUTES}")
        output_trip = kwargs.get("output_trip", f"{OUTPUT}/{day}.{OUTPUT_TRIP}")
        output_timestate = kwargs.get("output_timestate", f"{OUTPUT}/{day}.{OUTPUT_TIMESTATE}")
        threads = kwargs.get("threads", 40)

        f = open(f"{path}/{file}", "w")
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
    <input>
        <net-file value="{path}/{network}" />
        <additional-files value="{path}/{polygons}, {path}/{pt_stops}"/>
        <route-files value="{path}/{people_routes}, {path}/{pt_routes}" />
    </input>
    <output>
        <tripinfo-output value="{path}/{output_trip}" />
        <person-summary-output value="{path}/{output_timestate}" />
    </output>
    <processing>
        <threads value="{threads}" />
        <ignore-accidents value="True" />
        <collision.action value="teleport" />
        <pedestrian.model value="nonInteracting" />
    </processing>
    <routing>
    </routing>
    <report>
        <verbose value="true"/>
        <no-step-log value="true"/>
    </report>
    <gui_only>
        <gui-settings-file value="{path}/{view}"/>
        <quit-on-end value="True" />
        <start value="True" />
    </gui_only>
</configuration>
        ''')
        f.close()

    def __setNetworkConfig (self, **kwargs) :

        path = self.getPath()
        osm = self.getOsm()
        file = kwargs.get("config_network", f"{SUMOFILES}/{CONFIG_NETWORK}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        pt_stops = kwargs.get("pt_stops", f"{SUMOFILES}/{PT_STOPS}")
        pt_lines = kwargs.get("pt_lines", f"{SUMOFILES}/{PT_LINES}")

        f = open(f"{path}/{file}", "w")
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/netconvertConfiguration.xsd">
    <input>
        <type-files value="/usr/share/sumo/data/typemap/osmNetconvert.typ.xml,/usr/share/sumo/data/typemap/osmNetconvertUrbanDe.typ.xml,/usr/share/sumo/data/typemap/osmNetconvertPedestrians.typ.xml"/>
        <osm-files value="{path}/{osm}"/>
    </input>
    <output>
        <output-file value="{path}/{network}"/>
        <output.street-names value="true"/>
        <output.original-names value="true"/>
        <ptstop-output value="{path}/{pt_stops}"/>
        <ptline-output value="{path}/{pt_lines}"/>
        <osm.stop-output.length value="20" />
    </output>
    <processing>
        <geometry.remove value="true"/>
        <roundabouts.guess value="true"/>
    </processing>
    <tls_building>
        <tls.discard-simple value="true"/>
        <tls.join value="true"/>
        <tls.guess-signals value="true"/>
        <tls.default-type value="actuated"/>
    </tls_building>
    <ramp_guessing>
        <ramps.guess value="true"/>
    </ramp_guessing>
    <edge_removal>
        <remove-edges.isolated value="true"/>
    </edge_removal>
    <junctions>
        <junctions.join value="true"/>
        <junctions.corner-detail value="5"/>
    </junctions>
    <pedestrian>
        <crossings.guess value="true"/>
    </pedestrian>
    <railway>
        <railway.topology.repair value="true"/>
    </railway>
    <report>
        <verbose value="true"/>
    </report>
</configuration>
        ''')
        f.close()

    def __setPolygonConfig (self, **kwargs):

        path = self.getPath()
        osm = self.getOsm()
        file = kwargs.get("config_polygon", f"{SUMOFILES}/{CONFIG_POLYGON}")
        polygons = kwargs.get("polygons", f"{SUMOFILES}/{POLYGONS}")
        polygon_types = kwargs.get("polygon_types", initDataPlace.setPolygonTypeSumoFromOSM(path, f"{SUMOFILES}/{POLYGON_TYPES}")) # default : "/usr/share/sumo/data/typemap/osmPolyconvert.typ.xml"

        f = open(f"{path}/{file}", "w")
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/polyconvertConfiguration.xsd">
    <input>
        <net-file value="network.net.xml"/>
        <osm-files value="{path}/{osm}"/>
        <osm.keep-full-type value="true"/>
        <shapefile.add-param value="true"/>
        <type-file value="{path}/{polygon_types}"/>
    </input>
    <output>
        <output-file value="{path}/{polygons}"/>
    </output>
    <report>
        <verbose value="true"/>
    </report>
</configuration>
        ''')
        f.close()

    def __setDayDuarouterConfig (self, day, **kwargs) :

        path = self.getPath()
        file = kwargs.get("config_duarouter", f"{SUMOFILES}/{day}.{CONFIG_DUAROUTER}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        people_trips = kwargs.get("people_trips", f"{SUMOFILES}/{day}.{PEOPLE_TRIPS}")
        people_temp_routes = kwargs.get("people_temp_routes", f"{SUMOFILES}/{day}.{PEOPLE_TEMP_ROUTES}")
        people_temp_alt_routes = kwargs.get("people_temp_alt_routes", f"{SUMOFILES}/{day}.{PEOPLE_TEMP_ALT_ROUTES}")
        people_routes = kwargs.get("people_routes", f"{SUMOFILES}/{day}.{PEOPLE_ROUTES}")
        pt_stops = kwargs.get("pt_stops" , f"{SUMOFILES}/{PT_STOPS}")
        threads = kwargs.get("threads", 40)

        f = open(f"{path}/{file}", "w")
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/duarouterConfiguration.xsd">')
    <input>
        <net-file value="{path}/{network}" />
        <additional-files value="{path}/{pt_stops}"/>
        <route-files value="{path}/{people_trips}" />
    </input>
    <output>
        <output-file value="{path}/{people_temp_routes}"/>
        <alternatives-output value="{path}/{people_temp_alt_routes}"/>
    </output>
    <processing>
        <repair value="true"/>
        <routing-threads value="{threads}"/>
        <ptline-routing value="true"/>
    </processing>
    <report>
        <ignore-errors value="true"/>
    </report>
</configuration>
        ''')
        f.close()


    def __setSumoView(self, **kwargs):

        path = self.getPath()
        file = kwargs.get("view", f"{SUMOFILES}/{VIEW}")
        delay = kwargs.get("delay", 10)

        f = open(f"{path}/{file}", "w")
        f.write(f'''<viewsettings>
    <scheme name="spreading">
        <edges laneEdgeMode="0" scaleMode="0" laneShowBorders="0" showBikeMarkings="0" showLinkDecals="0" showLinkRules="0" showRails="0" >
            <colorScheme name="uniform">
                <entry color="grey" name="sidewalk"/>
                <entry color="grey" name="road"/>
                <entry color="grey" name="bike lane"/>
                <entry color="grey" name="green verge"/>
                <entry color="grey" name="waterway"/>
                <entry color="grey" name="railway"/>
                <entry color="grey" name="rails on road"/>
                <entry color="grey" name="no passenger"/>
                <entry color="grey" name="closed"/>
                <entry color="grey" name="connector"/>
                <entry color="grey" name="forbidden"/>
            </colorScheme>
        </edges>
        <vehicles vehicleMode="1" vehicleQuality="1" vehicle_minSize="1.00" vehicle_exaggeration="2.00" vehicle_constantSize="0" >
            <colorScheme name="uniform">
                <entry color="255,255,154"/>
            </colorScheme>
        </vehicles>
        <persons personMode="0" personQuality="1" person_minSize="1.00" person_exaggeration="15.00" person_constantSize="0" person_constantSizeSelected="0" personName_show="1" personName_size="30.00" personName_color="blue" personName_bgColor="128,0,0,0" personName_constantSize="0">
            <colorScheme name="given person/type color">
                <entry color="red"/>
            </colorScheme>
            <colorScheme name="uniform">
                <entry color="red"/>
            </colorScheme>
            <colorScheme name="given/assigned person color">
                <entry color="red"/>
            </colorScheme>
            <colorScheme name="given/assigned type color">
                <entry color="red"/>
            </colorScheme>
        </persons>
        <containers>
        </containers>
        <junctions junctionMode="0" drawShape="0" drawCrossingsAndWalkingareas="0" >
            <colorScheme name="uniform">
                <entry color="grey"/>
                <entry color="grey" name="waterway"/>
                <entry color="grey" name="railway"/>
            </colorScheme>
        </junctions>
        <additionals />
        <pois>
        </pois>
        <polys polyType_show="0" >
            <colorScheme name="given polygon color">
                <entry color="blue"/>
            </colorScheme>
        </polys>
        <legend showSizeLegend="1" showColorLegend="0" showVehicleColorLegend="0"/>
    </scheme>
    <delay value="{delay}"/>
</viewsettings>
        ''')
        f.close()

    def initNetwork (self, **kwargs) :

        config_network = kwargs.get("config_network", f"{SUMOFILES}/{CONFIG_NETWORK}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")

        self.__setNetworkConfig(**kwargs)
        os.system(f"netconvert -c {config_network}")

        return network

    def initPolygon(self, **kwargs) :

        config_polygon = kwargs.get("config_polygon", f"{SUMOFILES}/{CONFIG_POLYGON}")

        self.__setPolygonConfig(**kwargs)
        os.system(f"polyconvert -c {config_polygon}")

    def initSumoView(self, **kwargs):

        self.__setSumoView(**kwargs)

    def setPtRoute(self, **kwargs) :

        path = self.getPath()
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        pt_stops = kwargs.get("pt_stops", f"{SUMOFILES}/{PT_STOPS}")
        pt_lines = kwargs.get("pt_lines", f"{SUMOFILES}/{PT_LINES}")
        pt_routes = kwargs.get("pt_routes", f"{SUMOFILES}/{PT_ROUTES}")
        pt_stopinfos = kwargs.get("pt_stopinfos", f"{path}/{SUMOFILES}/{PT_STOPINFOS}")
        pt_trips = kwargs.get("pt_trips", f"{path}/{SUMOFILES}/{PT_TRIPS}")
        pt_vehicles = kwargs.get("pt_vehicles", f"{path}/{SUMOFILES}/{PT_VEHICLES}")
        begin = kwargs.get("begin", 0)
        frequency = kwargs.get("frequency", 1500)

        os.system(f"python /usr/share/sumo/tools/ptlines2flows.py -n {network} -s {pt_stops} -l {pt_lines} -o {pt_routes} -t {pt_trips} -r {pt_vehicles} -i {pt_stopinfos} -b {begin} -p {frequency} --random-begin True --ignore-errors True -v True")

    def setDayPeopleRoute(self, day, **kwargs) :

        people_trips = kwargs.get("people_trips", f"{SUMOFILES}/{day}.{PEOPLE_TRIPS}")
        people_temp_routes = kwargs.get("people_temp_routes", f"{SUMOFILES}/{day}.{PEOPLE_TEMP_ROUTES}")
        people_temp_alt_routes = kwargs.get("people_temp_alt_routes", f"{SUMOFILES}/{day}.{PEOPLE_TEMP_ALT_ROUTES}")
        people_routes = kwargs.get("people_routes", f"{SUMOFILES}/{day}.{PEOPLE_ROUTES}")
        config_duarouter = kwargs.get("config_duarouter", f"{SUMOFILES}/{day}.{CONFIG_DUAROUTER}")

        HandlerScripts.initPeopleTrips(file=f"{self.getPath()}/{people_trips}", day=day)
        self.__setDayDuarouterConfig (day, **kwargs)
        print(f"{color.GREEN}Building day people routes from day people trips in progress ...{color.RESET}")
        os.system (f"duarouter -c {config_duarouter}")
        #os.system(f"python /usr/share/sumo/tools/route/routecheck.py {network} --fix {temp_people_route}")
        print(f"{color.GREEN}Order day people routes by their time start in progress ...{color.RESET}")
        os.system(f"python /usr/share/sumo/tools/route/sort_routes.py {people_temp_routes} -o {people_routes}")

    def initDaySumoConfig (self, day, **kwargs) :

        self.__setDaySumoConfig(day, **kwargs)

    def runDay (self, day, show=False, **kwargs) :

        config_sumo = kwargs.get("config_sumo", f"{SUMOFILES}/{day}.{CONFIG_SUMO}")

        if show == True :
            os.system(f"sumo-gui -c {config_sumo}")
        else :
            os.system(f"sumo -c {config_sumo}")
