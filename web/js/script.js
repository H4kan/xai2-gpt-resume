function triggerUpload() {
    document.getElementById("fileInput").click();
}

function submitForm() {
    $("form").hide();
    $("form+p").hide();

    $("p+div").show();
    document.getElementById("uploadForm").submit();
}
