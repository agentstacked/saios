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

export const reelSchema = z.object({
  slug: z.string(),
  format: z.literal("reel"),
  hook: z.string(),
  cta: z.string(),
  terminalMp4: z.string(),
  voiceoverMp3: z.string(),
  voiceoverBeats: z.array(z.string()),
  voiceoverDurations: z.array(z.number()),
  music: z.string(),
});

const FPS = 30;
const HOOK_S = 1.2;
const CTA_S = 2;

export const Reel: React.FC<z.infer<typeof reelSchema>> = ({
  hook,
  cta,
  terminalMp4,
  voiceoverMp3,
  voiceoverDurations,
  music,
}) => {
  const audioFrames = Math.ceil(voiceoverDurations.reduce((a, b) => a + b, 0) * FPS);
  const ctaFrames = CTA_S * FPS;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0d0d", color: "#f5f5f5", fontFamily: "Inter, sans-serif" }}>
      <AbsoluteFill>
        <OffthreadVideo
          src={`file://${terminalMp4}`}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 70%, rgba(0,0,0,0.7) 100%)" }} />
      </AbsoluteFill>

      <Audio src={`file://${voiceoverMp3}`} />
      {music ? <Audio src={staticFile(`music/${music}`)} volume={0.12} /> : null}

      <Sequence durationInFrames={Math.ceil(HOOK_S * FPS)}>
        <Hook text={hook} />
      </Sequence>

      <Sequence from={audioFrames} durationInFrames={ctaFrames}>
        <CTA text={cta} />
      </Sequence>
    </AbsoluteFill>
  );
};

const Hook: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const y = interpolate(frame, [0, 8], [40, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 220 }}>
      <div
        style={{
          fontSize: 84,
          fontWeight: 900,
          lineHeight: 1.05,
          textAlign: "center",
          padding: "0 80px",
          transform: `translateY(${y}px)`,
          textShadow: "0 4px 24px rgba(0,0,0,0.6)",
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

const CTA: React.FC<{ text: string }> = ({ text }) => {
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 240 }}>
      <div
        style={{
          fontSize: 56,
          fontWeight: 800,
          textAlign: "center",
          padding: "32px 56px",
          backgroundColor: "rgba(0,0,0,0.55)",
          borderRadius: 24,
          whiteSpace: "pre-line",
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
