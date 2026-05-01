import { z } from "zod";
import {
  AbsoluteFill,
  OffthreadVideo,
  Audio,
  Sequence,
  useCurrentFrame,
  interpolate,
  staticFile,
} from "remotion";

export const walkthroughSchema = z.object({
  slug: z.string(),
  format: z.literal("walkthrough"),
  hook: z.string(),
  cta: z.string(),
  terminalMp4: z.string(),
  voiceoverMp3: z.string(),
  voiceoverBeats: z.array(z.string()),
  voiceoverDurations: z.array(z.number()),
  music: z.string(),
});

const FPS = 30;
const INTRO_S = 3;
const OUTRO_S = 4;

export const Walkthrough: React.FC<z.infer<typeof walkthroughSchema>> = ({
  hook,
  cta,
  terminalMp4,
  voiceoverMp3,
  voiceoverDurations,
  music,
}) => {
  const introFrames = INTRO_S * FPS;
  const audioFrames = Math.ceil(voiceoverDurations.reduce((a, b) => a + b, 0) * FPS);
  const outroFrames = OUTRO_S * FPS;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0d0d", color: "#f5f5f5", fontFamily: "Inter, sans-serif" }}>
      <Sequence durationInFrames={introFrames}>
        <Hook text={hook} />
      </Sequence>

      <Sequence from={introFrames} durationInFrames={audioFrames}>
        <AbsoluteFill>
          <OffthreadVideo src={`file://${terminalMp4}`} />
        </AbsoluteFill>
        <Audio src={`file://${voiceoverMp3}`} />
        {music ? <Audio src={staticFile(`music/${music}`)} volume={0.15} /> : null}
      </Sequence>

      <Sequence from={introFrames + audioFrames} durationInFrames={outroFrames}>
        <Outro text={cta} />
      </Sequence>
    </AbsoluteFill>
  );
};

const Hook: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12, 75, 90], [0, 1, 1, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 120, opacity }}>
      <div style={{ fontSize: 96, fontWeight: 800, lineHeight: 1.05, textAlign: "center" }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

const Outro: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 120, opacity }}>
      <div style={{ fontSize: 64, fontWeight: 700, textAlign: "center", whiteSpace: "pre-line" }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
