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



