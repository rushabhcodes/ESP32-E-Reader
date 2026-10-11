import { assembly } from "tscircuit";
import modelUrl from "../assets/enclosure/display-panel.glb";
import connection from "../assets/enclosure/display-connection.json";

/** Raw SSD2677 panel. The generated GLB compensates assembly.screen's
 * connector-derived rotation; keep it paired with display-connection.json. */
export const Waveshare_3_97inch_ePaper_G = () => (
  <assembly.screen
    name="EPD1"
    connectsTo=".J2"
    width={`${connection.panel.width}mm`}
    height={`${connection.panel.height}mm`}
    modelUrl={modelUrl}
  />
);
