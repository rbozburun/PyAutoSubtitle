# Auto_Sub.py
Bu program video içerisindeki sesi text'e dönüştürüp altyazı olarak videoya eklemektedir. Güncel sürümde
punctuation desteklemediği için sabit akan, fazla vurgu bulunmayan textlerde düzgün çalışmaktadır. 

Punctuation desteği için OpenAI'ın Whisper API kullanarak kod güncellenmelidir. Contrubution'a açık bir proje :)

Gereksinimler ve config detayları aşağıda yer almaktadır.

### Usage
```bash
python -m pip install -r requirements.txt
```
```bash
python auto_sub.py -f input.mp4 -o output.mp4
```
 

### Requirements
- Python 3.12.0
- Varsayılan olarak google voice recognizition servisi kullanılmaktadır. Local whisper kullanılabilir, bunun için aşağıdaki komutla kurulması gerekir:
    - `python3 -m pip install SpeechRecognition[whisper-local]`
- ImageMagick (/lib/ dizininde portable olarak ImageMagick-7.1.1-43-portable-Q16-HDRI-x64 kullanılmaktadır, isteğe göre değiştirilebilir.)

### editor.conf Options
- Türkçe:
```conf
[RecognizerSettings]
language=tr
recognizer=google
```

- Ingilizce
```conf
[RecognizerSettings]
language=en
recognizer=google
```


