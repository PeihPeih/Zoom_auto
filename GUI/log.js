const socket = io('https://zoom-auto.onrender.com/ws');

socket.on('connect', ()=>{
    console.log('Connected to server');
})

socket.on('participant_joined', (data)=>{
    console.log('Participant info:', data)
})