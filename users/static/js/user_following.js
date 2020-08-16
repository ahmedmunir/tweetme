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
    document.querySelector('.follow_button').addEventListener('click', e => {
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
                document.querySelector('.follow_button').classList.remove('btn-primary');
                document.querySelector('.follow_button').classList.add('btn-danger');
                document.querySelector('.follow_button').innerHTML = "Unfollow";
            }
    
            // If unfollow process succeded
            else if(data['state'] == 'unfollow') {
                document.querySelector('.follow_button').classList.add('btn-primary');
                document.querySelector('.follow_button').classList.remove('btn-danger');
                document.querySelector('.follow_button').innerHTML = "Follow"; 

            }
        })
    })
}