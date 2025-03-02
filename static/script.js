document.getElementById('submit').addEventListener('click', connectToPython)
const ingredients = document.getElementById('ingredients_input')


async function connectToPython(){
    try {
    const response = await fetch("http://127.0.0.1:5000/application",
        {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body : JSON.stringify({ingredients : ingredients.value})

        }
    )

    if (!response.ok){
        throw new Error('HTTP error! status : ${response.status}')
    }
    const recipe = await response.json()
    
    document.getElementById("recipe").innerText = recipe.gen_recipe
    

}
catch{
    document.getElementById("recipe_name").innerText = "Error fetching recipe. Please try again."
}



    
}