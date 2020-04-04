
let on_page_load = function () {
};


// let save_data = function () {
//     console.log('save data function');
//     $.post(saveDataURL, {
//         stored_data: app.list_tweets_and_retweets.join()
//     }, function (response) {
//         // console.log('server response');
//         if (response.result == true) {
//             console.log('data saved corretly');
//         } else {
//             window.alert(response.error);
//         }
//     });
// }



let app = new Vue({
    el: "#index",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        label: 'none',
        data_loaded: true,
        test_mode: true
    },
    methods: {
        save_data: save_data,
        track_btn: track_btn
    }
});


on_page_load();

