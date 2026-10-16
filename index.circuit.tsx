/**
 * ESP32 E-Reader Rev. B
 *
 * Device assembly; board circuitry and layout live in reader-board.tsx.
 */

import { assembly } from "tscircuit";
import { SparkFun_PRT_13855 } from "./imports/SparkFun_PRT_13855";
import antennaEnvelopeUrl from "./assets/enclosure/antenna-envelope-DO-NOT-PRINT.glb";
import batteryLinerUrl from "./assets/enclosure/battery-liner-DO-NOT-PRINT.glb";
import batteryAdhesiveUrl from "./assets/enclosure/battery-adhesive-DO-NOT-PRINT.glb";
import { Waveshare_3_97inch_ePaper_G } from "./imports/Waveshare_3_97inch_ePaper_G";
import frontChassisUrl from "./assets/enclosure/front-chassis.glb";
import displayCushioningUrl from "./assets/enclosure/display-cushioning.glb";
import pcbCoverFastenersUrl from "./assets/enclosure/pcb-cover-fasteners.glb";
import rearCoverUrl from "./assets/enclosure/rear-cover.glb";

import { EReaderBoard } from "./reader-board";

export default function ESP32EReader() {
	return (
		<assembly.device name="ESP32_E_READER">
			<EReaderBoard />
			<Waveshare_3_97inch_ePaper_G />
			<SparkFun_PRT_13855 />
			<assembly.cadassembly
				name="wifi_antenna_envelope"
				cadModel={{ glbUrl: antennaEnvelopeUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="front_chassis"
				cadModel={{
					glbUrl: frontChassisUrl,
					modelUnitToMmScale: 1,
					showAsTranslucentModel: true,
				}}
			/>
			<assembly.cadassembly
				name="display_cushioning"
				cadModel={{ glbUrl: displayCushioningUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="battery_liner"
				cadModel={{ glbUrl: batteryLinerUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="battery_adhesive"
				cadModel={{ glbUrl: batteryAdhesiveUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="pcb_cover_fasteners"
				cadModel={{ glbUrl: pcbCoverFastenersUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="rear_cover"
				cadModel={{
					glbUrl: rearCoverUrl,
					modelUnitToMmScale: 1,
					showAsTranslucentModel: true,
				}}
			/>
		</assembly.device>
	);
}
