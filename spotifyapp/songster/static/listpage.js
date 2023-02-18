let search_results = []

const searchSong = () => {
    const querry = document.getElementById('querry').value;
    fetch(`/spotifyapi/search?query=${querry}`)
       .then(result => result.json())
       .then(result => {
        const container = document.getElementById('search-results');
        console.log(container);
        container.innerHTML = '';
        
        items = result['status'];
        if(items['error'] !== undefined) {
            console.log("error")
            return;
        }
        let index = 0;
        items.forEach(result => {
            const div = document.createElement('div');
            div.innerHTML = `
                <h2>${index} ${result.name}</h2>
                <p>By: ${result.artists.join(', ')}</p> 
                <p>Year: ${result.year}</p>
                <img src="${ result.track_cover.url}" alt="Track cover">
                <audio controls>
                    <source src="${ result.preview_url }" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            `
            container.appendChild(div);
            search_results.push(result)
            console.log(search_results);
            index++;
        });

        const search_form = document.getElementById('choose-result-form');
        search_form.style.display = "block";
         
       });
}

const addSong = () => {
    const search_index = document.getElementById('search_index').value;
    const writeup = document.getElementById('writeup').value;

    let params = (new URL(document.location)).searchParams;
    let listid = params.get("id");
    const data = search_results[search_index];
    const data_for_request = {
        'name': data.name,
        'artists': data.artists.join(', '),
        'year': data.year,
        'spotify_uri': data.spotify_uri,
        'listid': listid,
        'writeup': writeup,
        'img_url': data.track_cover.url
    } 
    fetch('/add_song', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify(data_for_request)
            
    })
    .then(res => res.json())
    .then(res => {
        console.log(res);
        if(res.error !== undefined) {
            console.log(res.error)
            return;
        }
        window.open(res.link);
    })

}

const choose_result_form = document.getElementById('choose-result-form');
const addSongBtn = document.getElementById('add-song-btn');

choose_result_form.addEventListener('submit', event => {
    event.preventDefault();
    addSong();
});

addSongBtn.addEventListener('click', event => {
    event.preventDefault();
    addSong();
});