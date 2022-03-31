<template>
  <div>
    <h1 class="page-title">Grocery List</h1>
    <div class="new-task-wrapper">
      <input
        type="text"
        placeholder="Type a new item"
        class="new-task-input"
        v-model="newItemInput"
        @keyup.enter="addItem"
      />
      <button class="new-task-button" @click="addItem">+ Add</button>
    </div>
    <nav>
      <ul class="tab-wrapper">
        <li class="tab-item is-active">
          <button class="tab-button" @click="setView('All')">
            All ({{ allItemsLength }})
          </button>
        </li>
        <li class="tab-item">
          <button class="tab-button" @click="setView('Current')">
            Current ({{ currentItemsLength }})
          </button>
        </li>
        <li class="tab-item">
          <button class="tab-button" @click="setView('Completed')">
            Purchased ({{ completedItemsLength }})
          </button>
        </li>
      </ul>
    </nav>
    <ul class="task-list">
      <li v-for="item in itemsInView" :key="item.name" class="task-list-item">
        <div class="task-list-checkbox-wrapper">
          <IconCheckCircle v-show="item.purchased" />
          <IconCircle v-show="!item.purchased" />
          <input
            type="checkbox"
            v-model="item.purchased"
            :checked="item.purchased"
            class="task-list-checkbox"
            @change="setAsPurchased(item.id)"
          />
        </div>
        <input
          v-if="item.edit"
          class="task-list-edit-input"
          type="text"
          v-model="item.name"
        />
        <p
          v-else
          class="task-list-text"
          :class="item.purchased ? 'is-complete' : ''"
        >
          {{ item.name }}
        </p>
        <div class="task-list-cta">
          <p>
            <IconEdit
              class="task-list-cta-icon"
              @click="editGroceryListItem(item.id)"
            />
            <span class="sr-only">Edit</span>
          </p>
          <p>
            <IconDelete
              class="task-list-cta-icon"
              @click="deleteItemFromGroceryListHandler(item.id)"
            />
            <span class="sr-only">Delete</span>
          </p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { computed, reactive, toRefs, onMounted } from "vue";
import IconCheckCircle from "./IconCheckCircle.vue";
import IconCircle from "./IconCircle.vue";
import IconDelete from "./IconDelete.vue";
import IconEdit from "./IconEdit.vue";
import * as dataManager from "../dataManager.js";

export default {
  name: "ManageItems",
  components: {
    IconCheckCircle,
    IconCircle,
    IconDelete,
    IconEdit,
  },

  setup() {
    const state = reactive({
      currentView: "All",
      newItemInput: "",
      groceryListItems: [],
    });

    const itemsViews = reactive({
      allItemsLength: computed(() => {
        return state.groceryListItems.length;
      }),
      currentItemsLength: computed(() => {
        return state.groceryListItems.filter((item) => item.purchased === false)
          .length;
      }),
      completedItemsLength: computed(() => {
        return state.groceryListItems.filter((item) => item.purchased === true)
          .length;
      }),
    });

    const itemsInView = computed(() => {
      if (state.currentView == "Current") {
        return state.groceryListItems.filter(
          (item) => item.purchased === false
        );
      } else if (state.currentView == "Completed") {
        return state.groceryListItems.filter((item) => item.purchased === true);
      } else {
        return state.groceryListItems;
      }
    });

    const setView = (viewLabel) => {
      state.currentView = viewLabel;
    };
    const editGroceryListItem = async (itemId) => {
      const index = state.groceryListItems.findIndex(
        (item) => item.id == itemId
      );
      console.log("Editing item", index);
      state.groceryListItems[index].edit = !state.groceryListItems[index].edit;
      if (!state.groceryListItems[index].edit) {
        const item = state.groceryListItems[index];
        const response = await dataManager.updateItemRequestRequest(item);
        state.groceryListItems = await checkResponseAndLoadGroceryLists(
          response
        );
      }
    };
    const setAsPurchased = async (itemId) => {
      const index = state.groceryListItems.findIndex(
        (item) => item.id == itemId
      );
      const item = state.groceryListItems[index];
      const response = await dataManager.updateItemRequestRequest(item);
      state.groceryListItems = await checkResponseAndLoadGroceryLists(response);
    };
    const addItem = async () => {
      const item = {
        grocery_list: 1, //With a proper router component configured this value can be dynamic
        name: state.newItemInput,
      };
      const response = await dataManager.saveItemRequest(item);
      state.groceryListItems = await checkResponseAndLoadGroceryLists(response);

      state.newItemInput = "";
    };

    const deleteItemFromGroceryListHandler = async (itemId) => {
      const response = await dataManager.deleteItemFromGroceryListRequest(
        itemId
      );
      state.groceryListItems = await checkResponseAndLoadGroceryLists(response);
    };
    onMounted(async () => {
      const groceryLists = await dataManager.getGroceryListDetailsRequest();
      state.groceryListItems = groceryLists;
    });

    const checkResponseAndLoadGroceryLists = async (response) => {
      if (response.ok) {
        return await dataManager.getGroceryListDetailsRequest();
      } else {
        alert("HTTP-Error: " + response.status);
      }
    };

    return {
      ...toRefs(state),
      ...toRefs(itemsViews),
      itemsInView,
      addItem,
      deleteItemFromGroceryListHandler,
      editGroceryListItem,
      setView,
      setAsPurchased,
    };
  },
};
</script>


<style>
html {
  background-color: #fbfbfb;
}

.task-list {
  padding: 0;
}

.task-list-checkbox-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-list-checkbox {
  position: absolute;
  left: -3px;
  bottom: 2px;
  opacity: 0;
}

.is-complete {
  color: #6b6b6b;
  font-style: italic;
}

.task-list-edit-input {
  border: none;
  font-size: 16px;
}

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

.task-list-cta {
  display: flex;
  column-gap: 16px;
}

.task-list-text {
  margin-left: 12px;
  font-weight: bold;
  flex: 1;
}

.task-list-cta-icon .icon-object {
  fill: #2d2d2d;
}

.task-list-cta-icon:hover .icon-object {
  fill: #0728bf;
}

.tab-item:hover .tab-button {
  color: #0728bf;
}

.task-list-checkbox-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-list-checkbox {
  position: absolute;
  left: -3px;
  bottom: 2px;
  opacity: 0;
}

.task-list {
  padding: 0;
}

.task-list-cta-icon {
  opacity: 0;
  transition: 0.2s opacity ease-in;
}

.task-list-cta-icon .icon-object {
  fill: #2d2d2d;
}

.task-list-cta-icon:hover .icon-object {
  fill: #0728bf;
}

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

.task-list-item:hover .task-list-cta-icon,
.task-list-item:focus .task-list-cta-icon {
  opacity: 1;
}

.task-list-cta {
  display: flex;
  column-gap: 16px;
}

.task-list-edit-input,
.task-list-text {
  margin-left: 12px;
  font-weight: bold;
  flex: 1;
  border: 0;
  font-size: 16px;
}

.task-list-text.is-complete {
  color: #6b6b6b;
  text-decoration: line-through;
}

.new-task-wrapper {
  display: flex;
}

.new-task-input {
  padding: 16px;
  font-weight: 600;
  color: #2d2d2d;
  flex: 1;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  border: 1px solid #f6f6f6;
  box-shadow: 2px 2px 8px 0 #c0c0c0;
  letter-spacing: 1px;
  font-size: 1rem;
}

.new-task-input:hover {
  border: 1px solid #0631f8;
}

.new-task-input::placeholder {
  color: #959595;
}

.new-task-button {
  background-color: #0631f8;
  color: #fff;
  padding: 18px 24px;
  font-weight: 900;
  border: 0;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  transition: 0.2s background ease-in;
  font-size: 1rem;
}

.new-task-button:hover {
  background-color: #082ac9;
}

.tab-wrapper {
  display: flex;
  column-gap: 30px;
  list-style: none;
  margin: 45px 0;
  padding: 0;
}

.tab-item {
  padding-bottom: 6px;
}

.tab-item.is-active {
  border-bottom: 3px solid #0631f8;
}

.tab-button {
  border: 0;
  background-color: transparent;
  color: #6b6b6b;
  letter-spacing: 1px;
  font-weight: bold;
  font-family: "Source Sans Pro";
  padding: 0;
}

.tab-button:hover {
  cursor: pointer;
}

.task-list {
  padding: 0;
}

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

.task-list-cta {
  display: flex;
  column-gap: 16px;
}

.task-list-text {
  margin-left: 12px;
  font-weight: bold;
  flex: 1;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>