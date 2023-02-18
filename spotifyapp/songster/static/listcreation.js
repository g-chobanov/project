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