const socket = io('https://zoom-auto.onrender.com/ws');

socket.on('connect', ()=>{
    console.log('Connected to server');
})

socket.on('meeting_participant', (data)=>{
    console.log('Participant info:', data)
})