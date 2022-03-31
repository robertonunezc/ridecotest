<script>
import ManageItems from "./components/ManageItems.vue";
import GroceryListLists from "./components/GroceryListLists.vue";
import Login from "./components/Login.vue";

const routes = {
  "/all-grocery-lists": GroceryListLists,
  "/": Login,
  "/grocerylist-details": ManageItems,
};
export default {
  data() {
    return {
      currentPath: window.location.hash,
    };
  },
  computed: {
    currentView() {
      return routes[this.currentPath.slice(1) || "/"] || NotFound;
    },
  },
  mounted() {
    window.addEventListener("hashchange", () => {
      this.currentPath = window.location.hash;
    });
  },
};
</script>

<template>
  <main class="main-wrapper">
    <a href="#/">Login</a> |
    <a href="#/all-grocery-lists">All Grocery Lists</a> |
    <component :is="currentView" />
  </main>
</template>
<style>
.main-wrapper {
  max-width: 600px;
  margin: 0 auto;
}
</style>
