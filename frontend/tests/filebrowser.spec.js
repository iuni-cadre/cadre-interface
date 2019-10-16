import { shallowMount } from '@vue/test-utils';
import FilebrowserMain from '../src/components/Filebrowser/FilebrowserMain.vue'; // name of your Vue component

let wrapper;

beforeEach(() => {
    wrapper = shallowMount(FilebrowserMain, {
        propsData: {},
        mocks: {},
        stubs: {},
        methods: {},
    });
});

afterEach(() => {
    wrapper.destroy();
});

describe('FilebrowserMain', () => {
    test('is a Vue instance', () => {
        expect(wrapper.isVueInstance).toBeTruthy();
    });
});
