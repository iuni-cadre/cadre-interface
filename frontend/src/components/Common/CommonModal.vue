<template>
    <div >
        <div
            class="modal"
            tabindex="-1"
            role="dialog"
            aria-labelledby="modalLabel"
            :class="{'modal-show': true}"
            @click.stop="close"
            
        >
            <div
                class="modal-dialog d-flex align-items-center justify-content-center"
                role="document"
            >
                <div :style="`min-width: ${modalWidth}`"
                    class="alert m-5"
                    :class="'alert-' + modalStyle"
                    @click.stop
                >
                    <div
                        v-if="modalTitle"
                        class="modal-header"
                    >
                        <h4 class="modal-title text-center">{{modalTitle}}</h4>
                        <button
                            type="button"
                            class="close float-right"
                            aria-label="Close"
                            @click.stop.prevent="close"
                        >
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="d-flex align-items-center">
                            <fa
                                v-if="modalType === 'error'"
                                class="float-left m-2 mr-4 fa fa-3x fa-exclamation-triangle"
                                icon="exclamation-triangle"
                                aria-hidden="true"
                            ></fa>

                            <slot></slot>
                        </div>
                        <button
                            class="btn mt-2 btn-lg"
                            :class="'btn-' + (okButtonStyle || modalStyle)"
                            v-if="okButtonLabel && !okInFooter"
                            @click.stop.prevent="ok"
                        >
                            <fa
                                v-if="modalType === 'delete'"
                                class="mr-2 fa fa-trash"
                                :icon="['fas', 'trash-alt']"
                                aria-hidden="true"
                            ></fa>
                            {{okButtonLabel}}
                        </button>
                    </div>
                    <div class="modal-footer" :class="{' d-flex justify-content-between' : okInFooter }">
                        <button
                            class="btn"
                            :class="'btn-' + (okButtonStyle || modalStyle)"
                            v-if="okButtonLabel && okInFooter"
                            @click.stop.prevent="ok"
                        >
                            <fa
                                v-if="modalType === 'delete'"
                                class="mr-2 fa fa-trash"
                                :icon="['far', 'trash-alt']"
                                aria-hidden="true"
                            ></fa>
                            {{okButtonLabel}}
                        </button>

                        <button
                            class="btn"
                            :class="'btn-' + (closeButtonStyle || modalStyle)"
                            @click.stop.prevent="close"
                        >{{closeButtonLabel}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        modalStyle: {
            type: String,
            default: "info",
            validator: function(value) {
                return (
                    [
                        "info",
                        "primary",
                        "secondary",
                        "success",
                        "danger",
                        "warning"
                    ].indexOf(value) !== -1
                );
            }
        },
        modalType: {
            type: String,
            default: "",
            validator: function(value) {
                return ["", "error", "success", "delete"].indexOf(value) !== -1;
            }
        },
        modalTitle: {
            type: String
        },
        okButtonLabel: {
            type: String,
            default: ""
        },
        closeButtonLabel: {
            type: String,
            default: "Close"
        },
        visible: {
            type: Boolean
        },
        okInFooter: {
            default: false,
            type: Boolean
        },
        closeButtonStyle: {
            type: String
        },
        okButtonStyle: {
            type: String
        },
        modalWidth: {
            type: String,
            default: ""
        }
    },
    data: function() {
        return {
            // visible: true
        };
    },
    methods: {
        close: function() {
            this.$emit("close");
        },
        ok: function() {
            this.$emit("ok");
        },
        stop: function() {}
    }
};
</script>


<style lang="scss" scoped>
.modal-show {
    display: block;
    z-index: 2000;
}
.modal {
    background: rgba(0, 0, 0, 0.5);
    // opacity: 0;
    transition: opacity 0.1s linear;
}
.alert {
    position: relative;
    z-index: 3100;
    max-height: 100vh;
    overflow: auto;
}
.modal-dialog {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    z-index: 3000;
    pointer-events: all;
    max-height: 100vh;
    max-width: 90vw;
}
.modal-body {
    overflow: auto;
    max-height: 75vh;
    width: 100%;
}
.modal-content {
    font-size: 0.875rem;
    position: absolute;
    top: 3rem;
    bottom: 3rem;
    left: 3rem;
    right: 3rem;
    overflow: auto;
}
</style>
