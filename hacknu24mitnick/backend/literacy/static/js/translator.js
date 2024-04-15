document.getElementById('translate-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    // Get the text to translate and target language
    const textToTranslate = document.getElementById('source-text').value;
    const sourceLanguage = document.getElementById('source-lang').value;
    const targetLanguage = document.getElementById('target-lang').value;

    // Translate the text using an API
    translateText(textToTranslate, sourceLanguage, targetLanguage)
        .then(translatedText => {
            // Display the translated text
            document.getElementById('translated-text').innerText = translatedText;
        })
        .catch(error => {
            console.error('Translation error:', error);
            document.getElementById('translated-text').innerText = 'Error translating text';
        });
});



async function translateText(text, sourceLanguage, targetLanguage) {

    const response = await fetch("http://localhost:8000/translate", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            texts: text,
            sourceLanguageCode: sourceLanguage,
            targetLanguageCode: targetLanguage
        }),
    });

    const data = await response.json();

    return data.translations[0].text;
}