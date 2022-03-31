const getTokenFromStorage = () => {
    const token = window.localStorage.getItem("token");
    return `Bearer ${token}`
}
const saveItemRequest = async (item) => {
    const response = await fetch("http://localhost:8000/api/v1/grocery_list/item", {
        method: 'POST',
        headers: {
            'Authorization': getTokenFromStorage(),
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(item)
    })
    return response
}
const updateItemRequestRequest = async (item) => {
    console.log("Finish edit")
    const response = await fetch(`http://localhost:8000/api/v1/grocery_list/item/${item.id}`, {
        method: 'PUT',
        headers: {
            Authorization: getTokenFromStorage(),
            'Content-Type': 'application/json;charset=utf-8'

        },
        body: JSON.stringify(item)
    })
    return response
}
const deleteItemFromGroceryListRequest = async (itemId) => {
    console.log("Deleting item")
    const response = await fetch(`http://localhost:8000/api/v1/grocery_list/item/${itemId}`, {
        method: 'DELETE',
        headers: {
            Authorization: getTokenFromStorage()
        }
    })
    return response
};
const getGroceryListDetailsRequest = async () => {
    //With a proper router component configured the URL value can be dynamic
    console.log("GET ALL GL")
    const response = await fetch("http://localhost:8000/api/v1/grocery_list/1", {
        headers: {
            Authorization: getTokenFromStorage()
        }
    })
    if (response.ok) {
        // get the response body (the method explained below)
        let json = await response.json();
        return json.items
    } else {
        alert("HTTP-Error: " + response.status);
    }

}


const login = async (username, password) => {
    const response = await fetch("http://localhost:8000/api/v1/api-token-auth/", {
        method: 'POST',
        headers: {
            'Authorization': getTokenFromStorage(),
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({ username, password })
    })
    if (response.ok) {
        const token = await response.json()
        window.localStorage.setItem('token', token.token)
    } else {
        alert("HTTP-Error: " + response.status);
    }
}


export {
    saveItemRequest,
    updateItemRequestRequest,
    deleteItemFromGroceryListRequest,
    getGroceryListDetailsRequest,
    login
}