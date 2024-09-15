
const popup = document.querySelector('.chat-popup');
const chatBtn = document.querySelector('.chat-btn');
const submitBtn = document.querySelector('.submit');
const chatArea = document.querySelector('.chat-area');
const inputElm = document.querySelector('input');
const emojiBtn = document.querySelector('#emoji-btn');
const picker = new EmojiButton();


// Emoji selection  
window.addEventListener('DOMContentLoaded', () => {
   picker.on('emoji',emoji =>{
    document.querySelector('input').value += emoji;
   });

   emojiBtn.addEventListener('click', () =>{
    picker.togglePicker(emojiBtn);
   });

});


document.addEventListener('DOMContentLoaded', function() {
    // Show the chat button after 15 seconds
    setTimeout(function() {
        var chatButton = document.getElementById('chatIcon');
        if (chatButton) {
            chatButton.style.display = 'block'; // Show the chat button
        }
    }, 15000); // 15 seconds

    // Make the chat button draggable
    const chatIcon = document.getElementById('chatIcon');

    chatIcon.addEventListener('mousedown', function(e) {
        e.preventDefault();
        const shiftX = e.clientX - chatIcon.getBoundingClientRect().left;
        const shiftY = e.clientY - chatIcon.getBoundingClientRect().top;

        function moveAt(pageX, pageY) {
            chatIcon.style.left = pageX - shiftX + 'px';
            chatIcon.style.top = pageY - shiftY + 'px';
        }

        // Move the chat icon on mouse move
        function onMouseMove(e) {
            moveAt(e.pageX, e.pageY);
        }

        document.addEventListener('mousemove', onMouseMove);

        // Drop the chat icon on mouse up
        document.addEventListener('mouseup', function() {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', this);
        }, { once: true });
    });

    // Prevent default drag behavior
    chatIcon.ondragstart = function() {
        return false;
    };
});

//chat Button toggler

chatBtn.addEventListener('click',() =>{
    popup.classList.toggle('show');
});

//send message

submitBtn.addEventListener('click', ()=>{
    let userInput = inputElm.value;
    console.log(userInput);

    let temp = `<div class="out-msg">
    <span class="my-msg">${userInput}</span>
    <img src="image/me.jpg" class="avatar">
    </div>`

    chatArea.insertAdjacentHTML("beforeend",temp);
    inputElm.value='';
})