function resizeTextarea(){
    const textarea = document.getElementById('myTextarea');
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
}