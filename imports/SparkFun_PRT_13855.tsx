import { assembly } from "tscircuit";
import packUrl from "../assets/enclosure/battery-pack.glb";
import leadsUrl from "../assets/enclosure/battery-leads.glb";
import plugUrl from "../assets/enclosure/battery-plug.glb";

/** External pack and installed harness; BT1 is the separately assembled header. */
export function SparkFun_PRT_13855() {
	return <>
		<assembly.cadassembly name="battery_pack" cadModel={{ glbUrl: packUrl, modelUnitToMmScale: 1 }} />
		<assembly.cadassembly name="battery_leads" cadModel={{ glbUrl: leadsUrl, modelUnitToMmScale: 1 }} />
		<assembly.cadassembly name="battery_plug" cadModel={{ glbUrl: plugUrl, modelUnitToMmScale: 1 }} />
	</>;
}
