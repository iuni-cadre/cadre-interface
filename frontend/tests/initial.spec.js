import { shallowMount } from "@vue/test-utils";
import TestRunner from "jest-runner";
import { exportAllDeclaration } from "@babel/types";

let wrapper;

beforeEach(() => {
    // wrapper = shallowMount();
});

afterEach(() => {
    // wrapper.destroy();
});

describe("Test Suite", () => {
    test("is running", () => {
        expect(true).toBeTruthy();
    });
});
