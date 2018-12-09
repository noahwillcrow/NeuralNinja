// Spectron testing for front-end UI

const Application = require('spectron').Application;
const path = require('path');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');

var electronPath = path.join(__dirname, '..', 'node_modules', '.bin', 'electron');

if (process.platform === 'win32') {
    electronPath += '.cmd';
}

var appPath = path.join(__dirname, '..');

var app = new Application({
            path: electronPath,
            args: [appPath]
        });

global.before(function () {
    chai.should();
    chai.use(chaiAsPromised);
});

describe('Test Example', function () {
  beforeEach(function () {
  	this.timeout(0);
      return app.start();
  });

  afterEach(function () {
  	this.timeout(10000);
      return app.stop();
  });
  it('opens a window', function () {
    return true;
  });

  it('tests the title', function () {
    return app.client.waitUntilWindowLoaded()
      .getTitle().should.eventually.equal('NEURAL NINJA - Neural Network Visualizer');
  });

  it('tests the create button', function () {
    return app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
  });
    it('tests reaching network view page', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
      return app.client.waitForExist('#input-dropdown')
      .click("#create-button")
      .getText('.title').should.eventually.equal('Network');
  });

    it('tests selecting input and output nodes', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      return app.client.waitForExist("#train-button");
  });

   it('tests reaching training page', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      return app.client.waitForExist("#train-button").click("#train-button");
  });

  it('tests the increment button', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      return app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".increment-button")
      .click(".increment-button").click(".increment-button");
  });
  it('tests the decrement button', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      return app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".decrement-button")
      .click(".decrement-button").click(".decrement-button").click(".decrement-button")
      .click(".decrement-button").click(".decrement-button").click(".decrement-button");
  });

  it('tests the add layer button', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      return app.client.waitForExist("#train-button").click(".add-layer-button")
  });

  it('tests the add layer button', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      app.client.waitForExist("#train-button").click("#neural-network-canvas")
      return app.client.waitForExist("#matrix-canvas").click(".backward")
  });

  it('Stress test increment/decrement', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      return app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click(".decrement-button")
      .click(".decrement-button").click(".decrement-button").click(".decrement-button")
      .click(".decrement-button").click(".decrement-button").click(".decrement-button")
      .click(".add-layer-button").click("#train-button");
  });

    it('Stress test 2 matrix', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".increment-button").click("#neural-network-canvas")
      return app.client.waitForExist("#matrix-canvas").click(".backward");
  });

  it('Stress test 3 train page', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".decrement-button")
      .click(".add-layer-button").click("#train-button");
      return app.client.waitForExist(".file-choice-box").click(".backward")
  });

    it('Stress test 4 training page', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
       app.client.waitForExist('#input-dropdown');
      var input = app.client.elementIdText('#input-dropdown');
      input.keys('23');
      var output = app.client.elementIdText('#output-dropdown');
      input.keys('21');
      app.client.waitForExist(".title").click("#create-button");
      app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".decrement-button")
      .click(".add-layer-button").click("#train-button");
      return app.client.waitForExist(".file-choice-box")
  });

  it('Stress test 5 double pages', function () {
      app.client.waitUntilWindowLoaded()
      .click("#create-button")
      .getText('.title').should.eventually.equal('Create');
      app.client.waitForExist(".title").click("#create-button");
      app.client.waitForExist("#train-button").click(".increment-button")
      .click(".increment-button").click(".decrement-button")
      .click(".increment-button").click(".decrement-button")
      .click(".increment-button").click(".decrement-button")
      .click(".add-layer-button").click("#train-button");
      app.client.waitForExist(".file-choice-box").click(".backward")
      app.client.waitForExist("#train-button").click("#neural-network-canvas")
      return app.client.waitForExist("#matrix-canvas").click(".backward");
  });


});