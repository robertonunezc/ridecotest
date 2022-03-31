<template>
  <div>
    <h1 class="page-title">Grocery Lists</h1>
    <ul>
      <li
        v-for="groceryList in groceryLists"
        :key="groceryList.name"
        class="task-list-item"
      >
        <a href="#/grocerylist-details" class="task-list-text">{{
          groceryList.name
        }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
import { computed, reactive, toRefs, onMounted } from "vue";

export default {
  name: "GroceryListLists",
  setup() {
    const state = reactive({
      groceryLists: [],
    });
    const groceryLists = computed(() => {
      return state.groceryLists;
    });
    const getGroceryLists = async () => {
      console.log("Fetching data");
      const token = window.localStorage.getItem("token");

      const response = await fetch(
        "http://localhost:8000/api/v1/grocery_list/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (response.ok) {
        // get the response body (the method explained below)
        const json = await response.json();
        state.groceryLists = json.results;
      } else {
        alert("HTTP-Error: " + response.status);
      }
    };
    onMounted(() => {
      getGroceryLists();
    });
    return {
      ...toRefs(state),
      groceryLists,
    };
  },
};
</script>

<style scoped>
.task-list-item {
  border: 1px solid #f6f6f6;
  box-shadow: 2px 2px 8px 0 #cfcfcf;
  border-radius: 8px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  margin-bottom: 16px;
}

.task-list-item:hover {
  border: 1px solid #0631f8;
}
a {
  text-decoration: none;
}
.task-list-text {
  margin-left: 12px;
  font-weight: bold;
  padding: 10px;
  flex: 1;
  color: black;
}
</style>