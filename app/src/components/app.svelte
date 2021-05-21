<App { ...f7params } >

  <!-- Left panel with cover effect-->
  <Panel left cover themeDark>
    <View>
      <Page>
        <Navbar title="Left Panel"/>
        <Block>Left panel content goes here</Block>
      </Page>
    </View>
  </Panel>


  <!-- Right panel with reveal effect-->
  <Panel right reveal themeDark>
    <View>
      <Page>
        <Navbar title="我的"/>
        <Block>右侧面板</Block>
      </Page>
    </View>
  </Panel>


  <!-- Views/Tabs container -->
  <Views tabs class="safe-areas">
    <!-- Tabbar for switching views-tabs -->
    <Toolbar tabbar labels bottom>
      <Link tabLink="#view-prediction" tabLinkActive iconIos="f7:sun_haze_fill" iconAurora="f7:sun_haze_fill" iconMd="f7:sun_haze_fill" text="预测" />
      <Link tabLink="#view-calendar" iconIos="f7:calendar_today" iconAurora="f7:calendar_today" iconMd="f7:calendar_today" text="情感日历" />
      <Link tabLink="#view-shopping" iconIos="f7:cart_fill" iconAurora="f7:cart_fill" iconMd="f7:cart_fill" text="运势强化" />
      <Link tabLink="#view-shopping" iconIos="f7:heart_fill" iconAurora="f7:heart_fill" iconMd="f7:heart_fill" text="情侣版" />
    </Toolbar>

    <!-- Your main view/tab, should have "view-main" class. It also has "tabActive" prop -->
    <View id="view-home" main tab tabActive url="/" />

    <!-- Catalog View -->
    <View id="view-catalog" name="catalog" tab url="/catalog/" />

    <!-- Settings View -->
    <View id="view-settings" name="settings" tab url="/settings/" />

  </Views>


  <!-- Popup -->
  <Popup id="my-popup">
    <View>
      <Page>
        <Navbar title="Popup">
          <NavRight>
            <Link popupClose>Close</Link>
          </NavRight>
        </Navbar>
        <Block>
          <p>Popup content goes here.</p>
        </Block>
      </Page>
    </View>
  </Popup>

  <LoginScreen id="my-login-screen">
    <View>
      <Page loginScreen>
        <LoginScreenTitle>Login</LoginScreenTitle>
        <List form>
          <ListInput
            type="text"
            name="username"
            placeholder="Your username"
            bind:value={username}
          />
          <ListInput
            type="password"
            name="password"
            placeholder="Your password"
            bind:value={password}
          />
        </List>
        <List>
          <ListButton title="Sign In" onClick={() => alertLoginData()} />
        </List>
        <BlockFooter>
          Some text about login information.<br />Click "Sign In" to close Login Screen
        </BlockFooter>
      </Page>
    </View>
  </LoginScreen>
</App>
<script>
  import { onMount } from 'svelte';
  import { getDevice }  from 'framework7/lite-bundle';
  import {
    f7,
    f7ready,
    App,
    Panel,
    Views,
    View,
    Popup,
    Page,
    Navbar,
    Toolbar,
    NavRight,
    Link,
    Block,
    BlockTitle,
    LoginScreen,
    LoginScreenTitle,
    List,
    ListItem,
    ListInput,
    ListButton,
    BlockFooter
  } from 'framework7-svelte';
  import cordovaApp from '../js/cordova-app';

  import routes from '../js/routes';
  import store from '../js/store';

  const device = getDevice();
  // Framework7 Parameters
  let f7params = {
    name: '易生', // App name
    theme: 'md', // Automatic theme detection


    id: 'io.framework7.myapp', // App bundle ID
    // App store
    store: store,
    // App routes
    routes: routes,
    // Register service worker
    serviceWorker: {
      path: '/service-worker.js',
    },

    // Input settings
    input: {
      scrollIntoViewOnFocus: device.cordova && !device.electron,
      scrollIntoViewCentered: device.cordova && !device.electron,
    },
    // Cordova Statusbar settings
    statusbar: {
      iosOverlaysWebView: true,
      androidOverlaysWebView: false,
    },
  };
  // Login screen demo data
  let username = '';
  let password = '';

  function alertLoginData() {
    f7.dialog.alert('Username: ' + username + '<br>Password: ' + password, () => {
      f7.loginScreen.close();
    });
  }
  onMount(() => {
    f7ready(() => {
      // Init cordova APIs (see cordova-app.js)
      if (f7.device.cordova) {
        cordovaApp.init(f7);
      }

      // Call F7 APIs here
    });
  })
</script>