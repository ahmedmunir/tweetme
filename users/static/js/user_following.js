//GET CSRF Token
const getCookie =  name =>  {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Follow or UnFollow
if(document.querySelector('.follow_button')){
    document.querySelectorAll('.follow_button').forEach(follow_button => {
        console.log(follow_button);
        follow_button.addEventListener('click', e => {
            e.preventDefault();
        
            let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/follow/`;
            let data = new FormData();
            let state = follow_button.innerHTML;
            let target = e.target.closest('.user_container').dataset.username;
            data.append('state', state);
            data.append('target', target);
        
            fetch(url, {
                method: 'POST',
                body: data,
        
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                
                // If follow process succeded 
                if(data['state'] == 'follow') {
                    console.log('Entered Follow');
                    follow_button.classList.remove('follow');
                    follow_button.classList.add('unfollow');
                    follow_button.innerHTML = "Unfollow";
                    
                    // Increase number of followers in case that the logged in user
                    // visiting the page of his following
                    if(document.querySelector('.edit_button')){
                        document.querySelector('.following').textContent =
                        parseInt(document.querySelector('.following').textContent) + 1;
                    }

                }
        
                // If unfollow process succeded
                else if(data['state'] == 'unfollow') {
                    follow_button.classList.add('follow');
                    follow_button.classList.remove('unfollow');
                    follow_button.innerHTML = "Follow";
                    
                    // Decrease number of followers in case that the logged in user
                    // visiting the page of his following
                    if(document.querySelector('.edit_button')){
                        document.querySelector('.following').textContent =
                        parseInt(document.querySelector('.following').textContent) - 1;
                    }
    
                }
            })
        })
    })

}

// Follow or UnFollow for the owner of followers page
if(document.querySelector('.owner_follow_button')){
    document.querySelector('.owner_follow_button').addEventListener('click', e => {
        e.preventDefault();
    
        let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/follow/`;
        let data = new FormData();
        let state = document.querySelector('.follow_button').innerHTML;
        let target = e.target.closest('.user_container').dataset.username;
        data.append('state', state);
        data.append('target', target);
    
        fetch(url, {
            method: 'POST',
            body: data,
    
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            
            // If follow process succeded 
            if(data['state'] == 'follow') {
                document.querySelector('.owner_follow_button').classList.remove('follow');
                document.querySelector('.owner_follow_button').classList.add('unfollow');
                document.querySelector('.owner_follow_button').innerHTML = "Unfollow";
                
                // Increase number of followers for the owner of followers page
                document.querySelector('.followers').textContent =
                parseInt(document.querySelector('.followers').textContent) + 1;
            }
    
            // If unfollow process succeded
            else if(data['state'] == 'unfollow') {
                document.querySelector('.owner_follow_button').classList.add('follow');
                document.querySelector('.owner_follow_button').classList.remove('unfollow');
                document.querySelector('.owner_follow_button').innerHTML = "Follow";
                
                // Decrease number of followers for the owner of followers page
                document.querySelector('.followers').textContent =
                parseInt(document.querySelector('.followers').textContent) - 1;
            }
        })
    })
}