// Transcribe un audio (opus, m4a, mp3, wav…) a texto en español con Whisper small, sin bajar nada de Hugging Face.
// El modelo viene del paquete de npm sts-whisper-small (Whisper small en ONNX, q8).
// Uso: bash scripts/transcribir/transcribir.sh <audio> [<audio> …]
import { pipeline, env } from '@huggingface/transformers';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
env.allowRemoteModels = false;
env.localModelPath = path.resolve(process.env.STT_DIR || '.', 'node_modules/sts-whisper-small/models');
const asr = await pipeline('automatic-speech-recognition', 'Xenova/whisper-small', { dtype: 'q8' });
for (const archivo of process.argv.slice(2)) {
  const raw = execFileSync('ffmpeg', ['-v', 'quiet', '-i', archivo, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], { maxBuffer: 1 << 30 });
  const audio = new Float32Array(raw.buffer, raw.byteOffset, raw.length / 4);
  const out = await asr(audio, { language: 'spanish', task: 'transcribe', chunk_length_s: 30, stride_length_s: 5 });
  console.log(`### ${path.basename(archivo)}\n${out.text.trim()}\n`);
}
