import Globals from "../../CadreGlobalsPlugin";
// import axios from "axios";
import Vue from "vue";

// import CryptoJS from "crypto-js";

const MAX_LOADING_TIME = 30000;
const MIN_LOADING_TIME = 500;

export default {

    namespaced: true,
    state: {
        loading_queue: {},
        loading_timeout: 0
    },
    getters: {
        is_loading(state){
            const is_loading = !!Object.keys(state.loading_queue).length;
            // console.debug("is loading: ", is_loading);
            return is_loading;
        },
        loading_queue(state){
            return state.loading_queue;
        }
    },
    mutations: {
        addKey(state, {key, message}){
            // console.debug("Add Key: ", key)
            if(!key)
            {
                console.warn("Key is required for loading. Canceling.");
                return false;
            }

            if (!state.loading_queue[key]) {
                // this.loading_queue[key] = 0;
                Vue.set(state.loading_queue, key, {
                    interval: 0,
                    timer: 0,
                    cooldown_timeout: 0,
                    message: ""
                });
                state.loading_queue[key].interval = setInterval(() => {
                    /*
                        we need to keep track of how long this key has been
                        loading so we can show the spinner for at least a minimum
                        amount of time.
                    */
                    state.loading_queue[key].timer += 100;
                }, 100);
            } else {
                /* 
                    Handles a race condition if we add the key again during the "cooldown" time,
                    we need to cancel the old cooldown timer so that 
                    it doesn't cancel the NEW instance when it thinks it's
                    canceling the old instance.  So just cancel the cooldown
                    and keep going.
                */
                clearTimeout(state.loading_queue[key].cooldown_timeout);
            }
            state.loading_queue[key].message = message || "";
        },
        removeKey(state, {key}){
            // console.debug("Remove Key: ", key);
            if (state.loading_queue[key] !== undefined) {
                /*
                    we want to make sure that the spinner is shown for at least half a second
                    for UX purposes.  So it's not just a flash and people can't see it.
                    If the given key has been loading for more than the minimum time, just go 
                    ahead and call the callback.  Otherwise, we need to keep spinning for the 
                    min load time minus the time it's already been spinning during the actual
                    loading.
                */
                let cooldown_time = Math.max(
                    MIN_LOADING_TIME - state.loading_queue[key].timer,
                    1
                );
                /*
                    After the given cooldown time cancel the time tracking interval,
                    the cooldown timeout, and remove the key from the loading queue.
                */
                state.loading_queue[key].cooldown_timeout = setTimeout(() => {
                    if (state.loading_queue[key]) {
                        clearInterval(state.loading_queue[key].interval);
                        clearTimeout(state.loading_queue[key].cooldown_timeout);
                        Vue.delete(state.loading_queue, key);
                    } else {
                        console.warn(
                            `Loading queue key "${key}" was not found.`
                        );
                    }
                }, cooldown_time);
            }
        }
    },
}