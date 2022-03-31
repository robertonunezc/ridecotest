<template>
  <div>
    <form action="" @submit.prevent="login">
      <div class="flex">
        <input type="text" v-model="username" placeholder="username" />
        <input type="password" v-model="password" placeholder="password" />
        <button>Login</button>
      </div>
    </form>
  </div>
</template>

<script>
import { reactive, toRefs } from "vue";
import * as dataManager from "../dataManager.js";

export default {
  name: "Login",
  setup() {
    const state = reactive({
      username: "",
      password: "",
    });
    const login = async () => {
      await dataManager.login(state.username, state.password);
      window.location.href = "/#/all-grocery-lists";
    };

    return {
      ...toRefs(state),
      login,
    };
  },
};
</script>

<style scoped>
.flex {
  display: flex;
  flex-direction: column;
}
input {
  padding: 16px;
  font-weight: 600;
  color: #2d2d2d;
  flex: 1;
  border-radius: 8px;
  border: 1px solid #f6f6f6;
  box-shadow: 2px 2px 8px 0 #c0c0c0;
  letter-spacing: 1px;
  font-size: 1rem;
  margin: 10px 0;
}

button {
  background-color: #0631f8;
  color: #fff;
  padding: 18px 24px;
  font-weight: 900;
  border: 0;
  border-radius: 8px;
  transition: 0.2s background ease-in;
  font-size: 1rem;
}
</style>