document.getElementById('submit').addEventListener('click', sendImage)


async function sendImage(){
    console.log(1)
    const image = document.getElementById('input_image').files[0]
    const username = document.getElementById('username').value

    const formData = new FormData()
    formData.append('image', image)
    formData.append('username', username)
    console.log(formData['username'])

    const dataPacket = {
        method : 'POST',
        credentials : 'include',
        body : formData
    }


    const response = await fetch('http://localhost:5000/handle_image',dataPacket )

    if (response.ok){

        const data = await response.json()
        document.getElementById('gen-img').src = `${data.image_url}?${new Date().getTime()}`;

        console.log(data.image_url)
    }
    console.log(response.status)
    
    
    

    



}