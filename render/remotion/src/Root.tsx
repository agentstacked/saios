import { Composition, getInputProps } from "remotion";
import { Walkthrough, walkthroughSchema } from "./Walkthrough";
import { Reel, reelSchema } from "./Reel";

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  const props = getInputProps() as {
    voiceoverDurations?: number[];
    format?: "walkthrough" | "reel";
  };
  const totalAudio = (props.voiceoverDurations ?? [60]).reduce((a, b) => a + b, 0);
  const intro = 3;
  const outro = 4;
  const durationInFrames = Math.ceil((intro + totalAudio + outro) * FPS);

  return (
    <>
      <Composition
        id="Walkthrough"
        component={Walkthrough}
        durationInFrames={durationInFrames}
        fps={FPS}
        width={1920}
        height={1080}
        schema={walkthroughSchema}
        defaultProps={{
          slug: "demo",
          format: "walkthrough" as const,
          hook: "",
          cta: "",
          terminalMp4: "",
          voiceoverMp3: "",
          voiceoverBeats: [] as string[],
          voiceoverDurations: [] as number[],
          music: "",
        }}
      />
      <Composition
        id="Reel"
        component={Reel}
        durationInFrames={durationInFrames}
        fps={FPS}
        width={1080}
        height={1920}
        schema={reelSchema}
        defaultProps={{
          slug: "demo",
          format: "reel" as const,
          hook: "",
          cta: "",
          terminalMp4: "",
          voiceoverMp3: "",
          voiceoverBeats: [] as string[],
          voiceoverDurations: [] as number[],
          music: "",
        }}
      />
    </>
  );
};
