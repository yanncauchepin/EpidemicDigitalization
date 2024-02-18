import os
import sys
#from modules.scripts import ScriptsHandler
from modules.tools.style import Color


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare 'SUMO_HOME' environment variable.")


SUMOFILES = "modules/sumomobility/sumomobility_files"
SUMOOUTPUTS = "modules/sumomobility/sumomobility_outputs"

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

INDIVIDUALS_TRIPS = "individuals.trips.xml"
INDIVIDUALS_TEMP_ROUTES = "individuals.temp.routes.xml"
INDIVIDUALS_TEMP_ALT_ROUTES = "individuals.temp.alt.routes.xml"
INDIVIDUALS_ROUTES = "individuals.routes.xml"
CONFIG_DUAROUTER = "individuals.duaconfig"

OUTPUT_TRIP = "tripinfo.xml"
OUTPUT_TIMESTATE = "timestate.xml"

CONFIG_SUMO = "spreading.sumocfg"


class SumomobilityHandler():

    def __init__(self, root_path, osm_file, **kwargs) :
        self.osm_file = str(osm_file)
        self.root_path = str(root_path)
        os.makedirs(os.path.dirname(f'{SUMOFILES}'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{SUMOOUTPUTS}'), exist_ok=True)
        self.clear_sumomobility_files()
    
    def clear_sumomobility_files(self) :
        print(f"{Color.CYAN}Cleaning sumomobility files and outputs in progress ...{Color.RESET}")
        path = self.root_path
        for file in os.listdir(f'{path}/{SUMOFILES}') :
            file_path = os.path.join(f'{path}/{SUMOFILES}', f'{file}')
            os.remove(file_path)
        for file in os.listdir(f'{path}/{SUMOOUTPUTS}') :
            file_path = os.path.join(f'{path}/{SUMOOUTPUTS}', f'{file}')
            os.remove(file_path)

    def run_day (self, day, verbose=False, **kwargs) :
        day_config_sumo = kwargs.get("config_sumo", f"{SUMOFILES}/{day}.{CONFIG_SUMO}")
        if verbose == True :
            os.system(f"sumo-gui -c {day_config_sumo}")
        else :
            os.system(f"sumo -c {day_config_sumo}")

    def get_output_trips_file(self, **kwargs) :
        output_trip = kwargs.get("output_trip", f"{SUMOOUTPUTS}/{day}.{OUTPUT_TRIP}")
        return output_trip

    def init_network (self, **kwargs) :
        config_network = kwargs.get("config_network", f"{SUMOFILES}/{CONFIG_NETWORK}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        self.__set_config_network(**kwargs)
        os.system(f"netconvert -c {config_network}")
        return network

    def init_polygon(self, **kwargs) :
        config_polygon = kwargs.get("config_polygon", f"{SUMOFILES}/{CONFIG_POLYGON}")
        self.__set_config_polygon(**kwargs)
        os.system(f"polyconvert -c {config_polygon}")

    def init_sumomobility_view(self, **kwargs):
        self.__set_sumomobility_view(**kwargs)

    def init_pt_routes(self, **kwargs) :
        path = self.root_path
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

    def init_day_config_sumomobility (self, day, **kwargs) :
        self.__set_day_config_sumomobility(day, **kwargs)

    def init_day_individuals_routes(self, scriptshandler, day, **kwargs) :
        path = self.root_path
        #network
        day_individuals_trips = kwargs.get("day_individuals_trips", f"{SUMOFILES}/{day}.{INDIVIDUALS_TRIPS}")
        day_individuals_temp_routes = kwargs.get("day_individuals_temp_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_TEMP_ROUTES}")
        day_individuals_temp_alt_routes = kwargs.get("day_individuals_temp_alt_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_TEMP_ALT_ROUTES}")
        day_individuals_routes = kwargs.get("day_individuals_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_ROUTES}")
        day_config_duarouter = kwargs.get("day_config_duarouter", f"{SUMOFILES}/{day}.{CONFIG_DUAROUTER}")

        scriptshandler.init_individuals_trips(f"{path}/{day_individuals_trips}", day)
        self.__set_day_config_duarouter(day, **kwargs)
        print(f"{Color.CYAN}Building day individuals routes from day individuals trips "
              f"in progress ...{Color.RESET}")
        os.system (f"duarouter -c {day_config_duarouter}")
        #os.system(f"python /usr/share/sumo/tools/route/routecheck.py {network} --fix {day_individuals_temp_routes}")
        print(f"{Color.CYAN}Ordering day individuals routes by their start time in "
              f"progress ...{Color.RESET}")
        os.system(f"python /usr/share/sumo/tools/route/sort_routes.py {day_individuals_temp_routes} -o {day_individuals_routes}")

    def __set_day_config_sumomobility (self, day, **kwargs) :
        path = self.root_path
        day_config_sumo = kwargs.get("day_config_sumo", f"{SUMOFILES}/{day}.{CONFIG_SUMO}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        polygons = kwargs.get("polygons", f"{SUMOFILES}/{POLYGONS}")
        view = kwargs.get("view", f"{SUMOFILES}/{VIEW}")
        pt_stops = kwargs.get("pt_stops", f"{SUMOFILES}/{PT_STOPS}")
        day_individuals_routes = kwargs.get("day_individuals_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_ROUTES}")
        pt_routes = kwargs.get("pt_routes", f"{SUMOFILES}/{PT_ROUTES}")
        output_trip = kwargs.get("output_trip", f"{SUMOOUTPUTS}/{day}.{OUTPUT_TRIP}")
        output_timestate = kwargs.get("output_timestate", f"{SUMOOUTPUTS}/{day}.{OUTPUT_TIMESTATE}")
        threads = kwargs.get("threads", 40)
        file = open(f"{path}/{day_config_sumo}", "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
    <input>
        <net-file value="{path}/{network}" />
        <additional-files value="{path}/{polygons}, {path}/{pt_stops}"/>
        <route-files value="{path}/{day_individuals_routes}, {path}/{pt_routes}" />
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
        file.close()

    def __set_config_network (self, **kwargs) :
        path = self.root_path
        osm = self.osm_file
        config_network = kwargs.get("config_network", f"{SUMOFILES}/{CONFIG_NETWORK}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        pt_stops = kwargs.get("pt_stops", f"{SUMOFILES}/{PT_STOPS}")
        pt_lines = kwargs.get("pt_lines", f"{SUMOFILES}/{PT_LINES}")
        file = open(f"{path}/{config_network}", "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
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
        file.close()


    def __set_polygon_type_from_osm(self):
        path = self.root_path
        polygon_types = f"{SUMOFILES}/{POLYGON_TYPES}"
        file = open(f"{path}/{polygon_types}", "w")
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<polygonTypes>\n'
                   '\t<polygonType id="building" name="building" '
                       'color="0.0,0.0,1.0" layer="1"/>\n'
                   '</polygonTypes>\n')
        file.close()
        return file


    def __set_config_polygon (self, **kwargs):
        path = self.root_path
        osm = self.osm_file
        config_polygon = kwargs.get("config_polygon", f"{SUMOFILES}/{CONFIG_POLYGON}")
        polygons = kwargs.get("polygons", f"{SUMOFILES}/{POLYGONS}")
        polygon_types = kwargs.get("polygon_types", self.__set_polygon_type_from_osm()) # default : "/usr/share/sumo/data/typemap/osmPolyconvert.typ.xml"
        file = open(f"{path}/{config_polygon}", "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
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
        file.close()

    def __set_day_config_duarouter (self, day, **kwargs) :
        path = self.root_path
        day_config_duarouter = kwargs.get("day_config_duarouter", f"{SUMOFILES}/{day}.{CONFIG_DUAROUTER}")
        network = kwargs.get("network", f"{SUMOFILES}/{NETWORK}")
        day_individuals_trips = kwargs.get("day_individuals_trips", f"{SUMOFILES}/{day}.{INDIVIDUALS_TRIPS}")
        day_individuals_temp_routes = kwargs.get("day_individuals_temp_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_TEMP_ROUTES}")
        day_individuals_temp_alt_routes = kwargs.get("day_individuals_temp_alt_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_TEMP_ALT_ROUTES}")
        day_individuals_routes = kwargs.get("day_individuals_routes", f"{SUMOFILES}/{day}.{INDIVIDUALS_ROUTES}")
        pt_stops = kwargs.get("pt_stops" , f"{SUMOFILES}/{PT_STOPS}")
        threads = kwargs.get("threads", 40)
        file = open(f"{path}/{day_config_duarouter}", "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/duarouterConfiguration.xsd">')
    <input>
        <net-file value="{path}/{network}" />
        <additional-files value="{path}/{pt_stops}"/>
        <route-files value="{path}/{day_individuals_trips}" />
    </input>
    <output>
        <output-file value="{path}/{day_individuals_temp_routes}"/>
        <alternatives-output value="{path}/{day_individuals_temp_alt_routes}"/>
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
        file.close()


    def __set_sumomobility_view(self, **kwargs):
        path = self.root_path
        view = kwargs.get("view", f"{SUMOFILES}/{VIEW}")
        delay = kwargs.get("delay", 10)
        file = open(f"{path}/{view}", "w")
        file.write(f'''<viewsettings>
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
        file.close()
