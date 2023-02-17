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
        items.forEach(result => {
            const div = document.createElement('div');
            console.log(result)
            div.innerHTML = `
                <h2>${result.name}</h2>
                <p>Artist:${result.artists.join(', ')}</p> 
                <p>Year:${result.year}</p>
                <img src="${ result.track_cover.url}" alt="Track cover">
                <audio controls>
                    <source src="${ result.preview_url }" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            `
            container.appendChild(div);
        });
         
       });
}

function authenticate_spotify() {
    fetch("/spotifyapi/is-authenticated")
        .then(res => res.json())
        .then(data => {
            if(!data.status) {
                fetch("/spotifyapi/get-auth-url")
                .then(res => res.json())
                .then(data => {
                    window.location.replace(data.url);
                })
            }
        });
}



