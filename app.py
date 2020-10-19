from spokestack.activation_timeout import ActivationTimeout
from spokestack.asr.speech_recognizer import CloudSpeechRecognizer
from spokestack.io.pyaudio import PyAudioInput, PyAudioOutput
from spokestack.nlu.tflite import TFLiteNLU
from spokestack.pipeline import SpeechPipeline
from spokestack.tts.clients.spokestack import TextToSpeechClient
from spokestack.tts.manager import TextToSpeechManager
from spokestack.vad.webrtc import VoiceActivityDetector
from spokestack.wakeword.tflite import WakewordTrigger

from config import KEY_ID, KEY_SECRET
from minecraft.dialogue_manager import DialogueManager
from minecraft.responses import Response


def main():
    pipeline = SpeechPipeline(
        PyAudioInput(frame_width=20, sample_rate=16000, exception_on_overflow=False),
        [
            VoiceActivityDetector(),
            WakewordTrigger(pre_emphasis=0.97, model_dir="tflite"),
            CloudSpeechRecognizer(spokestack_id=KEY_ID, spokestack_secret=KEY_SECRET),
            ActivationTimeout(),
        ],
    )

    nlu = TFLiteNLU("tflite")
    dialogue_manager = DialogueManager()
    manager = TextToSpeechManager(
        TextToSpeechClient(KEY_ID, KEY_SECRET), PyAudioOutput(),
    )

    @pipeline.event
    def on_activate(context):
        print("active")

    @pipeline.event
    def on_recognize(context):
        pipeline.pause()
        results = nlu(context.transcript)
        response = dialogue_manager(results)
        if response:
            manager.synthesize(response, "text", "demo-male")
        pipeline.resume()

        if results.intent == "AMAZON.StopIntent":
            pipeline.stop()

    manager.synthesize(Response.WELCOME.value, "text", "demo-male")
    pipeline.start()
    pipeline.run()


if __name__ == "__main__":
    main()
