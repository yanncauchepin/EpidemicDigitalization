import os
import sys
#from modules.scripts import ScriptsHandler
from modules.tools.style import Color


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare 'SUMO_HOME' environment variable.")


SUMOFILES = "sumomobility/input_files/"
SUMOOUTPUTS = "sumomobility/outputs_files/"

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
        self.osm = str(osm_file)
        self.root = str(root_path)
        self.sumo_files = kwargs.get("sumomobility_files", SUMOFILES)
        self.sumo_outputs = kwargs.get("sumomobility_outputs", SUMOOUTPUTS)
        
        self.config_network = kwargs.get("config_network", CONFIG_NETWORK)
        self.network = kwargs.get("network", NETWORK)
        
        self.config_polygon = kwargs.get("config_polygon", CONFIG_POLYGON)
        self.polygon_types = kwargs.get("polygon_types", POLYGON_TYPES)
        self.polygons = kwargs.get("polygons", POLYGONS)
        
        self.pt_stops = kwargs.get("pt_stops", PT_STOPS)
        self.pt_lines = kwargs.get("pt_lines", PT_LINES)
        self.pt_routes = kwargs.get("pt_routes", PT_ROUTES)
        self.pt_stopinfos = kwargs.get("pt_stopinfos", PT_STOPINFOS)
        self.pt_trips = kwargs.get("pt_trips", PT_TRIPS)
        self.pt_vehicles = kwargs.get("pt_vehicles", PT_VEHICLES)
        self.pt_begin = kwargs.get("pt_begin", 0)
        self.pt_frequency = kwargs.get("pt_frequency", 1500)
        
        self.config_duarouter = kwargs.get("config_duarouter", CONFIG_DUAROUTER)
        self.individuals_trips = kwargs.get("individuals_trips", INDIVIDUALS_TRIPS)
        self.individuals_temp_routes = kwargs.get("individuals_temp_routes", INDIVIDUALS_TEMP_ROUTES)
        self.individuals_temp_alt_routes = kwargs.get("individuals_temp_alt_routes", INDIVIDUALS_TEMP_ALT_ROUTES)
        self.individuals_routes = kwargs.get("individuals_routes", INDIVIDUALS_ROUTES)
        
        self.config_sumo = kwargs.get("config_sumo", CONFIG_SUMO)
        self.view = kwargs.get("view", VIEW)
        self.threads = kwargs.get("threads", 40)
        self.view = kwargs.get("view", VIEW)
        self.delay = kwargs.get("delay", 10)
                
        self.output_timestate = kwargs.get("output_timestate", OUTPUT_TIMESTATE)
        self.output_trip = kwargs.get("output_trip", OUTPUT_TRIP)
        
        os.makedirs(os.path.dirname(os.path.join(self.root, self.sumo_files)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.join(self.root, self.sumo_outputs)), exist_ok=True)
        self.clear_sumomobility_files()
    
    
    def clear_sumomobility_files(self) :
        print(f"{Color.CYAN}Cleaning sumomobility files and outputs in progress ...{Color.RESET}")
        for file in os.listdir(os.path.join(self.root, self.sumo_files)) :
            file_path = os.path.join(self.root, self.sumo_files, file)
            os.remove(file_path)
        for file in os.listdir(os.path.join(self.root,self.sumo_outputs)) :
            file_path = os.path.join(os.path.join(self.root, self.sumo_outputs, file))
            os.remove(file_path)


    def run_day (self, day, verbose=True) :
        day_config_sumo = f'{day}.{self.config_sumo}'
        day_config_sumo_ = os.path.join(self.root, self.sumo_files, day_config_sumo)
        if verbose == True :
            os.system(f"sumo-gui -c {day_config_sumo_}")
        else :
            os.system(f"sumo -c {day_config_sumo_}")


    def get_day_output_trips_file(self, day) :
        day_output_trip = f'{day}.{self.output_trip}'
        day_output_trip_ = os.path.join(self.root, self.sumo_outputs, day_output_trip)
        return day_output_trip_


    def init_network(self):
        config_network_ = os.path.join(self.root, self.sumo_files, self.config_network)
        network_ = os.path.join(self.root, self.sumo_files, self.network)
        self.__set_config_network()
        os.system(f"netconvert -c {config_network_} -o {network_}")
        return network_


    def init_polygon(self) :
        config_polygon_ = os.path.join(self.root, self.sumo_files, self.config_polygon)
        self.__set_polygon_type_from_osm()
        self.__set_config_polygon()
        os.system(f"polyconvert -c {config_polygon_}")


    def init_sumomobility_view(self):
        self.__set_sumomobility_view()


    def init_pt_routes(self) :
        network_ = os.path.join(self.root, self.sumo_files, self.network)
        pt_stops_ = os.path.join(self.root, self.sumo_files, self.pt_stops)
        pt_lines_ = os.path.join(self.root, self.sumo_files, self.pt_lines)
        pt_routes_ = os.path.join(self.root, self.sumo_files, self.pt_routes)
        pt_stopinfos_ = os.path.join(self.root, self.sumo_files, self.pt_stopinfos)
        pt_trips_ = os.path.join(self.root, self.sumo_files, self.pt_trips)
        pt_vehicles_ = os.path.join(self.root, self.sumo_files, self.pt_vehicles)
        pt_begin_ = self.pt_begin
        pt_frequency_ = self.pt_frequency
        os.system(f"python /usr/share/sumo/tools/ptlines2flows.py -n {network_} -s {pt_stops_} -l {pt_lines_} -o {pt_routes_} -t {pt_trips_} -r {pt_vehicles_} -i {pt_stopinfos_} -b {pt_begin_} -p {pt_frequency_} --random-begin True --ignore-errors True -v True")


    def init_day_config_sumomobility (self, day) :
        self.__set_day_config_sumomobility(day)


    def init_day_individuals_routes(self, scriptshandler, day) :
        network_ = os.path.join(self.root, self.sumo_files, self.network)
        day_individuals_trips = f'{day}.{self.individuals_trips}'
        day_individuals_trips_ = os.path.join(self.root, self.sumo_files, day_individuals_trips)
        day_individuals_temp_routes = f'{day}.{self.individuals_temp_routes}'
        day_individuals_temp_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_temp_routes)
        day_individuals_temp_alt_routes = f'{day}.{self.individuals_temp_alt_routes}'
        day_individuals_temp_alt_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_temp_alt_routes)
        day_individuals_routes = f'{day}.{self.individuals_routes}'
        day_individuals_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_routes)
        day_config_duarouter = f'{day}.{self.config_duarouter}'
        day_config_duarouter_ = os.path.join(self.root, self.sumo_files, day_config_duarouter)
       
        scriptshandler.init_individuals_trips(day_individuals_trips_, day)
        self.__set_day_config_duarouter(day)
        print(f"{Color.CYAN}Building day individuals routes from day individuals trips "
              f"in progress ...{Color.RESET}")
        os.system (f"duarouter -c {day_config_duarouter_}")
        #os.system(f"python /usr/share/sumo/tools/route/routecheck.py {network_} --fix {day_individuals_temp_routes_}")
        print(f"{Color.CYAN}Ordering day individuals routes by their start time in "
              f"progress ...{Color.RESET}")
        os.system(f"python /usr/share/sumo/tools/route/sort_routes.py {day_individuals_temp_routes_} -o {day_individuals_routes_}")


    def __set_day_config_sumomobility (self, day) :
        day_config_sumo = f'{day}.{self.config_sumo}'
        day_config_sumo_ = os.path.join(self.root, self.sumo_files, day_config_sumo)
        network_ = os.path.join(self.root, self.sumo_files, self.network)
        polygons_ = os.path.join(self.root, self.sumo_files, self.polygons)
        view_ = os.path.join(self.root, self.sumo_files, self.view)
        pt_stops_ = os.path.join(self.root, self.sumo_files, self.pt_stops)
        day_individuals_routes = f'{day}.{self.individuals_routes}'
        day_individuals_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_routes)
        pt_routes_ = os.path.join(self.root, self.sumo_files, self.pt_routes)
        day_output_trip = f'{day}.{self.output_trip}'
        day_output_trip_ = os.path.join(self.root, self.sumo_outputs, day_output_trip)
        day_output_timestate = f'{day}.{self.output_timestate}'
        day_output_timestate_ = os.path.join(self.root, self.sumo_outputs, day_output_timestate)
        threads_ = self.threads
        file = open(day_config_sumo_, "w")
        # <ignore--accident value='True'/>
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
    <input>
        <net-file value="{network_}" />
        <additional-files value="{polygons_}, {pt_stops_}"/>
        <route-files value="{day_individuals_routes_}, {pt_routes_}" />
    </input>
    <output>
        <tripinfo-output value="{day_output_trip_}" />
        <person-summary-output value="{day_output_timestate_}" />
    </output>
    <processing>
        <threads value="{threads_}" />
        <collision.action none />
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
        <gui-settings-file value="{view_}"/>
        <quit-on-end value="True" />
        <start value="True" />
    </gui_only>
</configuration>
        ''')
        file.close()


    def __set_config_network (self) :
        config_network_ = os.path.join(self.root, self.sumo_files, self.config_network)
        network_ = os.path.join(self.root, self.sumo_files, self.network)
        pt_stops_ = os.path.join(self.root, self.sumo_files, self.pt_stops)
        pt_lines_ = os.path.join(self.root, self.sumo_files, self.pt_lines)
        file = open(config_network_, "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/netconvertConfiguration.xsd">
    <input>
        <type-files value="/usr/share/sumo/data/typemap/osmNetconvert.typ.xml,/usr/share/sumo/data/typemap/osmNetconvertUrbanDe.typ.xml,/usr/share/sumo/data/typemap/osmNetconvertPedestrians.typ.xml"/>
        <osm-files value="{self.root}/{self.osm}"/>
    </input>
    <output>
        <output-file value="{network_}"/>
        <output.street-names value="true"/>
        <output.original-names value="true"/>
        <ptstop-output value="{pt_stops_}"/>
        <ptline-output value="{pt_lines_}"/>
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
        polygon_types_ = os.path.join(self.root, self.sumo_files, self.polygon_types)
        file = open(polygon_types_, "w")
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<polygonTypes>\n'
                   '\t<polygonType id="building" name="building" '
                       'color="0.0,0.0,1.0" layer="1"/>\n'
                   '</polygonTypes>\n')
        file.close()
        return file


    def __set_config_polygon (self):
        config_polygon_ = os.path.join(self.root, self.sumo_files, self.config_polygon)
        polygons_ = os.path.join(self.root, self.sumo_files, self.polygons)
        polygon_types_ = os.path.join(self.root, self.sumo_files, self.polygon_types) # default : "/usr/share/sumo/data/typemap/osmPolyconvert.typ.xml"
        file = open(config_polygon_, "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/polyconvertConfiguration.xsd">
    <input>
        <net-file value="network.net.xml"/>
        <osm-files value="{self.root}/{self.osm}"/>
        <osm.keep-full-type value="true"/>
        <shapefile.add-param value="true"/>
        <type-file value="{polygon_types_}"/>
    </input>
    <output>
        <output-file value="{polygons_}"/>
    </output>
    <report>
        <verbose value="true"/>
    </report>
</configuration>
        ''')
        file.close()
        

    def __set_day_config_duarouter (self, day) :
        network_ = os.path.join(self.root, self.sumo_files, self.network)
        day_config_duarouter = f'{day}.{self.config_duarouter}'
        day_config_duarouter_ = os.path.join(self.root, self.sumo_files, day_config_duarouter)
        day_individuals_trips = f'{day}.{self.individuals_trips}'
        day_individuals_trips_ = os.path.join(self.root, self.sumo_files, day_individuals_trips)
        day_individuals_temp_routes = f'{day}.{self.individuals_temp_routes}'
        day_individuals_temp_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_temp_routes)
        day_individuals_temp_alt_routes = f'{day}.{self.individuals_temp_alt_routes}'
        day_individuals_temp_alt_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_temp_alt_routes)
        day_individuals_routes = f'{day}.{self.individuals_routes}'
        day_individuals_routes_ = os.path.join(self.root, self.sumo_files, day_individuals_routes)
        pt_stops_ = os.path.join(self.root, self.sumo_files, self.pt_stops)
        threads_ = self.threads
        file = open(day_config_duarouter_, "w")
        file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/duarouterConfiguration.xsd">')
    <input>
        <net-file value="{network_}" />
        <additional-files value="{pt_stops_}"/>
        <route-files value="{day_individuals_trips_}" />
    </input>
    <output>
        <output-file value="{day_individuals_temp_routes_}"/>
        <alternatives-output value="{day_individuals_temp_alt_routes_}"/>
    </output>
    <processing>
        <repair value="true"/>
        <routing-threads value="{threads_}"/>
        <ptline-routing value="true"/>
    </processing>
    <report>
        <ignore-errors value="true"/>
    </report>
</configuration>
        ''')
        file.close()


    def __set_sumomobility_view(self):
        view_ = os.path.join(self.root, self.sumo_files, self.view)
        delay_ = self.delay
        file = open(view_, "w")
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
    <delay value="{delay_}"/>
</viewsettings>
        ''')
        file.close()
