
var data;

function findAllOccurrences(substring, string) {
    let index = string.indexOf(substring);
    const occurrences = [];

    while (index !== -1) {
        occurrences.push(index);
        index = string.indexOf(substring, index + 1);
    }

    return occurrences;
}

$( document ).ready(function() {
    
    let pattern = /Page \d+/g;

    let splitted = data.fText.split(pattern);
    splitted.shift();
    for (let i = 0; i < data.hls.length; i++)
    {
        let current_hl = data.hls[i];

        if (current_hl.page_num > splitted.length)
            continue;
        target_page = splitted[current_hl.page_num - 1];

        allIndexes = findAllOccurrences(current_hl.text, target_page)

        if (current_hl.occurrence > allIndexes.length)
            continue;

        target_idx = allIndexes[current_hl.occurrence - 1];
        
        let before = target_page.substring(0, target_idx);
        let after = target_page.substring(target_idx + current_hl.text.length);
        let replacement = `<span class="hl-span" id="${i}">${current_hl.text}</span>`;

        target_page = before + replacement + after;

        splitted[current_hl.page_num - 1] = target_page;
    }
    let whole_txt = splitted.join("\n").replaceAll("\n", "<br/>");
    $("#scrap-text")[0].innerHTML = whole_txt;

    setTimeout(() => {
        $(".hl-span").click(function() {
            $("#hl-text").text(data.hls[this.id].highlight);
        })
    })
});