/*
    =========
    Variables
    =========
*/
let tweetsElement = document.querySelector("#tweets");
let scrolled = false;
let start = 0

/*
    ================
    Event Listeners
    ================
*/

// Loading more data when reaching to the end of page
window.addEventListener('scroll', e => {
    if(window.scrollY + window.innerHeight >= document.body.offsetHeight) {
        
        // load more data from server
        if(scrolled == false) {
            fetchData();
            scrolled = true;
            
        }
    }
})


/*
==============
    Functions
==============
*/

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

//Display loading Icon
const loadingIcon = (state) => {
    if(state=="hide"){
        document.querySelector('.loading_icon').remove();
    }
    else if(state="show"){
        let icon = document.createElement('h2');
        icon.classList.add('loading_icon');
        tweetsElement.insertAdjacentElement('beforeend', icon);
    }
}

// REACT tweet function
const react_tweet = (react_button) => {
    react_button.addEventListener('click', e => {
        e.preventDefault();

        let id = e.target.closest('.tweet_container').dataset.id;
        let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/tweets/${id}/react/`;
        let react = e.target.closest('a').dataset['react']
        let data = new FormData()
        data.append('react', react);

        // Send request
        fetch(url, {
            method: "POST",
            body: data,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if(response.redirected == true){
                alert("You need to login first to be able to react to Tweets!");
            } else {
                return response.json();
            }
        })
        .then(data => {

            // If tweet deleted before we react

            if (data != undefined) {
                if(data['message']) {
                    document.querySelector('.wrong-alert').innerHTML = data['message'];
                } else {
                    
                    targeted_element = e.target.closest('.text_buttons_container');
                    len_of_elements = targeted_element.childNodes.length

                    // Because we don't know if it is a retweet or normal Tweet
                    // we will depend existence of retweet_container class or not

                    if(targeted_element.innerHTML.includes('retweet_container')){

                        // Change link button state
                        targeted_element.childNodes[2].classList[data['like']]('react_color');
                        
                        // change number of likes
                        targeted_element.childNodes[3].innerHTML = data['likes'];
                        
                        // change dislike button state
                        targeted_element.childNodes[4].classList[data['dislike']]('react_color');
                        
                        // change number of dislikes
                        targeted_element.childNodes[5].innerHTML = data['dislikes'];
                    } else {

                        // Change link button state
                        targeted_element.childNodes[1].classList[data['like']]('react_color');
                        
                        // change number of likes
                        targeted_element.childNodes[2].innerHTML = data['likes'];
                        
                        // change dislike button state
                        targeted_element.childNodes[3].classList[data['dislike']]('react_color');
                        
                        // change number of dislikes
                        targeted_element.childNodes[4].innerHTML = data['dislikes'];

                    }
                }
            }
        })
    })
}

// DELETE Function 
const delete_event_listener = (delete_button) => {
    delete_button.addEventListener('click', e => {
        e.preventDefault();
        let id = e.target.closest('.tweet_container').dataset.id;
        let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/tweets/${id}/delete/`;

        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data['message'] == 'TweeT deleted successfully!'){
                e.target.closest('.tweet_container').remove();
                document.querySelector('.wrong-alert').innerHTML = data['message'];
            } else {
                document.querySelector('.wrong-alert').innerHTML = data['message'];
            }
        })
    })
}

// Edit function
const edit_event_listener = (tweet, e_event_handler) => {
    // Display backdrop window
    document.querySelector('.backdrop_window').style.display = 'block';

    // Display Form window with needed info
    let edit_form = document.createElement('div');
    edit_form.classList.add('edit_form');
    edit_form.setAttribute('data-id', tweet['id']);

    // Display Edit tweet form
    let edit_text = document.createElement('textarea');
    edit_text.classList.add('edit_text_textarea');
    edit_text.setAttribute('name', 'content');
    edit_text.setAttribute('id', 'id_content');
    edit_text.setAttribute('placeholder', 'Add a comment');
    edit_text.innerHTML = e_event_handler.target.closest('.text_buttons_container').childNodes[0].innerHTML;

    // Display retweet content if it is edit for retweet
    if(tweet['retweet']){

        var tweet_Element = document.createElement('div');
        tweet_Element.classList.add('row');
        tweet_Element.classList.add('tweet_container');
        
        let tweet_text_buttons = document.createElement('div');
        tweet_text_buttons.classList.add('text_buttons_container');

        // Tweet username
        let tweet_username = document.createElement('small');
        tweet_username.classList.add('tweet_username');
        tweet_username.innerHTML = `${tweet['retweeted_tweet']['user_first_name']} ${tweet['retweeted_tweet']['user_last_name']}`;

        // Tweet user unique name
        let tweet_unique_user = document.createElement('div');
        tweet_unique_user.classList.add('tweet_user_unique');
        tweet_unique_user.innerHTML = ` @${tweet['retweeted_tweet']['user_username']}`;
        
        let tweet_header = document.createElement('div');
        tweet_header.classList.add('row');
        
        let tweet_name_date = document.createElement('div');
        tweet_name_date.classList.add('rtname_date_container');   

        // Tweet Date
        let tweet_date = document.createElement('small');
        tweet_date.classList.add('tweet_date');
        tweet_date.innerHTML = tweet['retweeted_tweet']['date_posted'];

        // Tweet Text
        let tweet_text = document.createElement('p');
        tweet_text.classList.add('retweet_text');
        tweet_text.innerHTML = tweet['retweeted_tweet']['content'];

        // User image container
        let user_image = document.createElement('div');
        user_image.classList.add('col-md-auto');
        user_image.classList.add('image_container');
        let image_url = tweet['retweeted_tweet']['user_image'];
        let image = document.createElement('img');
        image.classList.add('user_tweet_image');
        image.setAttribute('src', image_url);
        user_image.insertAdjacentElement('afterbegin', image);

        tweet_name_date.insertAdjacentElement('beforeend', tweet_username);
        tweet_name_date.insertAdjacentElement('beforeend', tweet_date);
        tweet_name_date.insertAdjacentElement('beforeend', tweet_unique_user);
        tweet_header.insertAdjacentElement('beforeend', user_image);
        tweet_header.insertAdjacentElement('beforeend', tweet_name_date);
        tweet_Element.insertAdjacentElement('beforeend', tweet_header);
        tweet_Element.insertAdjacentElement('beforeend', tweet_text);
    }


    // Edit buttons & Event Listener
    let edit_button = document.createElement('button');
    edit_button.setAttribute('type', 'submit');
    edit_button.classList.add('btn');
    edit_button.classList.add('edit_submit');
    edit_button.innerHTML = 'Edit';
    // Add Event Listener for Edit button
    edit_button.addEventListener('click', e => {
        e.preventDefault();
        let id = e.target.closest('.edit_form').dataset.id;
        let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/tweets/${id}/edit/`;
        
        //Edit data AJAX request
        let data = new FormData();
        data.append('content', edit_text.value);
        fetch(url , {
            method: "POST",
            body: data,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data['message'] == 'Error') {
                alert(data['content'])
            } else {
                // Remove form
                edit_form.remove();

                // Disblay none for backgroun-window
                document.querySelector('.backdrop_window').style.display = 'none';

                // Edit all Tweets with that Id
                document.querySelectorAll(`[data-id="${id}"]`).forEach(tweet_to_edit => {
                    tweet_to_edit.childNodes[1].childNodes.forEach(edit_tweet_child => {
                        if(edit_tweet_child.className == "tweet_text" || edit_tweet_child.className == "retweet_text") {
                            edit_tweet_child.innerHTML = data['content'];
                        }
                    })
                })
            }
        })
    })

    // Cancel Edit Button & Event Listener
    let cancel_edit_button = document.createElement('button');
    cancel_edit_button.classList.add('btn');
    cancel_edit_button.classList.add('edit_cancel');
    cancel_edit_button.innerHTML = 'Cancel';
    // Add Event listener for cancel Button
    cancel_edit_button.addEventListener('click', e => {
        e.preventDefault();

        // Remove form
        edit_form.remove();

        // Disblay none for backgroun-window
        document.querySelector('.backdrop_window').style.display = 'none';
    })

    edit_form.insertAdjacentElement('beforeend', edit_text);
    
    //display tweet_element if exist
    if(tweet_Element){
        edit_form.insertAdjacentElement('beforeend', tweet_Element);
    } 
    
    edit_form.insertAdjacentElement('beforeend', cancel_edit_button);
    edit_form.insertAdjacentElement('beforeend', edit_button);

    //Insert edit
    document.querySelector('body').insertAdjacentElement('afterbegin', edit_form);
}

//
const retweet_function = (tweet) => {
    // Ensure that user is already logged in
    let user_check = false;
    document.querySelectorAll('.link_redirect').forEach(anchor_link => {
        if(anchor_link.getAttribute("href") == '/logout/') {
            user_check = true;
        }
    })

    if(user_check) {
        // Display backdrop window
        document.querySelector('.backdrop_window').style.display = 'block';

        //Display drop down window with needed info
        let retweet_form = document.createElement('form');
        retweet_form.classList.add('retweet_form');
        retweet_form.setAttribute('method', 'POST');
        retweet_form.setAttribute('action', `/tweets/${tweet['id']}/retweet/`);
        
        // CSRF Token
        let csrf_input = document.createElement('input');
        csrf_input.setAttribute('type', 'hidden');
        csrf_input.setAttribute('name', 'csrfmiddlewaretoken');
        csrf_input.setAttribute('value', getCookie('csrftoken'));

        // Retweet comment
        let retweet_comment = document.createElement('textarea');
        retweet_comment.setAttribute('name', 'content');
        retweet_comment.setAttribute('id', 'id_content');
        retweet_comment.setAttribute('placeholder', 'Add a comment');
        retweet_comment.classList.add('edit_text_textarea');

        // Tweet Element Container
        let tweet_Element = document.createElement('div');
        tweet_Element.classList.add('row');
        tweet_Element.classList.add('tweet_container');
        tweet_Element.setAttribute('name', 'id');
        tweet_Element.setAttribute('value', tweet['id']);

        // Tweet text & username container
        let tweet_text_buttons = document.createElement('div');
        tweet_text_buttons.classList.add('text_buttons_container');

        // Tweet username
        let tweet_username = document.createElement('small');
        tweet_username.classList.add('tweet_username');
        tweet_username.innerHTML = `${tweet['user_first_name']} ${tweet['user_last_name']}`;

        // Tweet user unique name
        let tweet_unique_user = document.createElement('div');
        tweet_unique_user.classList.add('tweet_user_unique');
        tweet_unique_user.innerHTML = ` @${tweet['user_username']}`;

        let tweet_header = document.createElement('div');
        tweet_header.classList.add('row');
        
        let tweet_name_date = document.createElement('div');
        tweet_name_date.classList.add('rtname_date_container');    
        // Tweet Date
        let tweet_date = document.createElement('small');
        tweet_date.classList.add('tweet_date');
        tweet_date.innerHTML = tweet['date_posted'];

        // Tweet Text
        let tweet_text = document.createElement('p');
        tweet_text.classList.add('retweet_text');
        tweet_text.innerHTML = tweet['content'];

        // User image container
        let user_image = document.createElement('div');
        user_image.classList.add('col-md-auto');
        user_image.classList.add('image_container');
        let image_url = tweet['user_image'];
        let image = document.createElement('img');
        image.classList.add('user_tweet_image');
        image.setAttribute('src', image_url);
        user_image.insertAdjacentElement('afterbegin', image);

        // Cancel and retweet buttons
        let retweet_button = document.createElement('button');
        retweet_button.setAttribute('type', 'submit');
        retweet_button.classList.add('btn');
        retweet_button.classList.add('retweet_submit');
        retweet_button.innerHTML = 'Retweet';
        let cancel_retweet_button = document.createElement('button');
        cancel_retweet_button.classList.add('btn');
        cancel_retweet_button.classList.add('retweet_cancel');
        cancel_retweet_button.innerHTML = 'Cancel';

        // Add Event listener for cancel Button
        cancel_retweet_button.addEventListener('click', e => {
            e.preventDefault();

            // Remove form
            retweet_form.remove();

            // Disblay none for backgroun-window
            document.querySelector('.backdrop_window').style.display = 'none';
        })

        tweet_name_date.insertAdjacentElement('beforeend', tweet_username);
        tweet_name_date.insertAdjacentElement('beforeend', tweet_date);
        tweet_name_date.insertAdjacentElement('beforeend', tweet_unique_user);
        tweet_header.insertAdjacentElement('beforeend', user_image);
        tweet_header.insertAdjacentElement('beforeend', tweet_name_date);
        tweet_Element.insertAdjacentElement('beforeend', tweet_header);
        tweet_Element.insertAdjacentElement('beforeend', tweet_text);
        retweet_form.insertAdjacentElement('beforeend', csrf_input);
        retweet_form.insertAdjacentElement('beforeend', retweet_comment);
        retweet_form.insertAdjacentElement('beforeend', tweet_Element);
        retweet_form.insertAdjacentElement('beforeend', cancel_retweet_button);
        retweet_form.insertAdjacentElement('beforeend', retweet_button);
        
        //Insert retweet_form
        document.querySelector('body').insertAdjacentElement('afterbegin', retweet_form);
    } else {
        alert("You need to login first to retweet!");
    }
}

// Fetch Tweets from server
const fetchData = () => {

    // Display Loading Icon while waiting to Fetch data from back-end
    loadingIcon('show');

    let params = new URLSearchParams({
        'start' : start,
        'search': document.querySelector('.search_input_tag').value
    })

    // Fetch data from server
    let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/tweets/?${params}`
    fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        
        // Hide Loading shape
        loadingIcon('hide');

        if(data['tweets'].length > 0){

            // Display tweets
            data['tweets'].forEach(tweet => {

                //Add new Tweet
                add_tweet_to_dom('beforeend', tweet);

                //set start to new value
                start = data['start'];

                //set scrolled to false again
                scrolled = false;
                
            });

        } else {
            let tweets_end = document.createElement('small');
            tweets_end.classList.add('tweets_end');
            tweets_end.innerHTML = "There are no more tweets to load";
            tweetsElement.insertAdjacentElement('beforeend', tweets_end);
        }
    })
}

// create new tweet function
const add_tweet_to_dom = (position, tweet) => {

    // Tweet Element Container
    let tweet_Element = document.createElement('div');
    tweet_Element.classList.add('tweet_container');
    tweet_Element.setAttribute('data-id', tweet['id']);
    

    // Tweet text & username container
    let tweet_text_buttons = document.createElement('div');
    tweet_text_buttons.classList.add('text_buttons_container');


    let tweet_header = document.createElement('div');
    tweet_header.classList.add('row');
    
    let tweet_name_date = document.createElement('div');
    tweet_name_date.classList.add('name_date_container');
    

    // Tweet username
    let tweet_username = document.createElement('a');
    tweet_username.classList.add('tweet_username');
    tweet_username.setAttribute('href', `/${tweet['user_username']}/`);
    tweet_username.innerHTML = `${tweet['user_first_name']} ${tweet['user_last_name']}`;

    // Tweet user unique name
    let tweet_unique_user = document.createElement('div');
    tweet_unique_user.classList.add('tweet_user_unique');
    tweet_unique_user.innerHTML = ` @${tweet['user_username']}`;

    // Tweet Date
    let tweet_date = document.createElement('small');
    tweet_date.classList.add('tweet_date');
    tweet_date.innerHTML = tweet['date_posted'];

    // Tweet Text
    let tweet_text = document.createElement('p');
    tweet_text.classList.add('tweet_text');
    tweet_text.innerHTML = tweet['content'];

    // Tweet Like button
    let like_button = document.createElement('a');
    like_button.classList.add('like_button');
    like_button.classList[tweet['liked']]('react_color');
    like_button.setAttribute('data-react', 'like');
    like_button.innerHTML = '<i class="fa fa-thumbs-up"></i>';
    react_tweet(like_button);

    // Number of likes
    let likes_number = document.createElement('span');
    likes_number.classList.add('likes_number');
    likes_number.innerHTML = tweet['likes'];

    // Tweet Dislike button
    let dislike_button = document.createElement('a');
    dislike_button.classList.add('dislike_button');
    dislike_button.classList[tweet['disliked']]('react_color');
    dislike_button.setAttribute('data-react', 'dislike');
    dislike_button.innerHTML = '<i class="fa fa-thumbs-down"></i>';
    react_tweet(dislike_button);

    // Number of Dislikes
    let dislikes_number = document.createElement('span');
    dislikes_number.classList.add('dislikes_number');
    dislikes_number.innerHTML = tweet['dislikes'];

    let delete_edit = document.createElement('div');
    delete_edit.classList.add('delete_edit_container');

    // Delete button
    if(tweet['tweet-owner'] === true) {

        // Add delete Button
        var delete_button = document.createElement('a');
        delete_button.classList.add('delete_tweet');
        delete_button.innerHTML = '<i class="fa fa-trash"></i>';

        // Add event listener to new DELETE Button
        delete_event_listener(delete_button);

        // Add Edit button
        var edit_button = document.createElement('a');
        edit_button.classList.add('edit_tweet');
        edit_button.innerHTML = '<i class="fa fa-edit"></i>';

        // Add event listener to new Edit button
        edit_button.addEventListener('click', e => {
            e.preventDefault();

            edit_event_listener(tweet, e);
        })
    }

    // Display Retweeted Tweet if it is a Retweet
    if(tweet['retweet']) {

        // Display Retweeted Tweet if the original tweet exists
        if(tweet['retweeted_tweet']){
            var retweet_container = document.createElement('a');
            retweet_container.classList.add('retweet_container');
            retweet_container.classList.add('row');
            retweet_container.setAttribute('data-id', tweet['retweeted_tweet']['id']);

            let retweet_Element = document.createElement('div');
            retweet_Element.classList.add('retext_container');
            

            // Retweet username
            let retweet_username = document.createElement('a');
            retweet_username.classList.add('retweet_username');
            retweet_username.setAttribute('href', `/${tweet['retweeted_tweet']['user_username']}`);
            retweet_username.innerHTML = `${tweet['retweeted_tweet']['user_first_name']} ${tweet['retweeted_tweet']['user_last_name']}`;

            // Retweet user unique name
            let retweet_unique_user = document.createElement('div');
            retweet_unique_user.classList.add('retweet_user_unique');
            retweet_unique_user.innerHTML = ` @${tweet['retweeted_tweet']['user_username']}`;

            let retweet_header = document.createElement('div');
            retweet_header.classList.add('row');
            
            let retweet_name_date = document.createElement('div');
            retweet_name_date.classList.add('rtname_date_container');        

            // Retweet Date
            let retweet_date = document.createElement('small');
            retweet_date.classList.add('retweet_date');
            retweet_date.innerHTML = tweet['retweeted_tweet']['date_posted'];

            // Retweet Text
            let retweet_text = document.createElement('p');
            retweet_text.classList.add('retweet_text');
            retweet_text.innerHTML = tweet['retweeted_tweet']['content'];

            // Retweet image
            // User image container
            let rt_user_image = document.createElement('div');
            rt_user_image.classList.add('col-md-auto');
            rt_user_image.classList.add('image_container');
            let rt_image_url = tweet['retweeted_tweet']['user_image'];
            let rt_image = document.createElement('img');
            rt_image.classList.add('user_tweet_image');
            rt_image.setAttribute('src', rt_image_url);
            rt_user_image.insertAdjacentElement('afterbegin', rt_image);

            //append data to retweet element
            retweet_Element.insertAdjacentElement('beforeend', retweet_header);
            retweet_header.insertAdjacentElement('beforeend', rt_user_image);
            retweet_header.insertAdjacentElement('beforeend', retweet_name_date);
            retweet_name_date.insertAdjacentElement('beforeend', retweet_username);
            retweet_name_date.insertAdjacentElement('beforeend', retweet_date);
            retweet_name_date.insertAdjacentElement('beforeend', retweet_unique_user);

            retweet_header.insertAdjacentElement('beforeend', retweet_text);
            retweet_container.insertAdjacentElement('beforeend', retweet_Element);
        } else {

            // Display Text that the original tweet is 
            var retweet_container = document.createElement('div');
            retweet_container.classList.add('retweet_container');
            retweet_container.classList.add('deleted_tweet');
            retweet_container.innerHTML = 'The original Tweet was deleted!';
        }
        
    } else {

        // Create retweet button
        var retweet_button = document.createElement('a');
        retweet_button.classList.add('retweet_tweet');
        retweet_button.innerHTML = '<i class="fa fa-retweet" aria-hidden="true"></i>';

        // Add retweet Event listener
        retweet_button.addEventListener('click', e => {
            e.preventDefault();
            retweet_function(tweet)
        });
        
    }

    

    // User image container
    let user_image = document.createElement('div');
    user_image.classList.add('col-md-auto');
    user_image.classList.add('image_container');
    let image_url = tweet['user_image'];
    let image = document.createElement('img');
    image.classList.add('user_tweet_image');
    image.setAttribute('src', image_url);
    user_image.insertAdjacentElement('afterbegin', image);

    // Insert All elements inside Div that will contain them

    tweet_header.insertAdjacentElement('beforeend', user_image);
    tweet_header.insertAdjacentElement('beforeend', tweet_name_date);
    tweet_name_date.insertAdjacentElement('beforeend', tweet_username);
    tweet_name_date.insertAdjacentElement('beforeend', tweet_date);
    tweet_name_date.insertAdjacentElement('beforeend', tweet_unique_user);

    tweet_text_buttons.insertAdjacentElement('beforeend', tweet_text);

    // add retweet container if exists
    if(retweet_container) {
        tweet_text_buttons.insertAdjacentElement('beforeend', retweet_container);
    }
    
    tweet_text_buttons.insertAdjacentElement('beforeend', like_button);
    tweet_text_buttons.insertAdjacentElement('beforeend', likes_number);
    tweet_text_buttons.insertAdjacentElement('beforeend', dislike_button);
    tweet_text_buttons.insertAdjacentElement('beforeend', dislikes_number);

    // Display Delete button if exists

    
    // add retweet button if there is not retweet
    if(!retweet_container) {
        tweet_text_buttons.insertAdjacentElement('beforeend', retweet_button);
    }
    if(tweet['tweet-owner'] === true){
        tweet_text_buttons.insertAdjacentElement('beforeend',delete_edit)
        delete_edit.insertAdjacentElement('beforeend', delete_button);
        delete_edit.insertAdjacentElement('beforeend', edit_button);
    }
    tweet_Element.insertAdjacentElement('beforeend', tweet_header);
    tweet_Element.insertAdjacentElement('beforeend', tweet_text_buttons);
    tweetsElement.insertAdjacentElement(position, tweet_Element);

}

fetchData();