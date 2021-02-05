'use strict'
// console.log('%c路漫漫','font-size:14px;color:#66ccff;');
/** ********
 *拓扑图组件初始配置说明
 *couldEdit:true,是否可以拖拽编辑，如果此项为false，则仅显示中央区域，且不可以进行拖拽
 *leftViewShow:true,是否需要显示左侧视图
 *centerViewShow:true,是否需要显示中央视图
 *rightViewShow:true,是否需要显示右侧视图
 *leftViewWidth:4,总比例等于24
 *centerViewWidth:16,总比例等于24
 *rightViewWidth:4,总比例等于24
 *mainBoxId : 'torp',初始渲染的父元素ID
 *canvasId : 'l000_torp000_canvas',动态插入的vanvas画布ID，防止id名冲突，可配置
 *elementType : [],默认拖拽元素的配置项格式为svg背景图样式，可配置
 *
****************/

function TopologyMap(para) {
  const baseConfig = {
    couldEdit: true,
    onlyDrag: false,
    leftViewShow: true,
    centerViewShow: true,
    rightViewShow: true,
    leftViewWidth: 4,
    centerViewWidth: 12,
    rightViewWidth: 8,
    mainBoxId: 'torp',
    canvasId: 'l000_torp000_canvas',
    elementType: [
      {
        name: '测试图形1',
        background_id: '001',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20height%3D%221000%22%20viewBox%3D%220%200%20750%20750.00178%22%20width%3D%221000%22%3E%3Cpath%20d%3D%22M549.934%20325.008h25v25h-25zm0%200M499.934%20325.008h25v25h-25zm0%200M449.934%20325.008h25v25h-25zm0%200M174.938%20325.008h25v25h-25zm0%200M549.934%20475.008h25v25h-25zm0%200M499.934%20475.008h25v25h-25zm0%200M449.934%20475.008h25v25h-25zm0%200M174.938%20475.008h25v25h-25zm0%200%22%2F%3E%3Cpath%20d%3D%22M137.438%20575.004c-6.903%200-12.497%205.598-12.497%2012.5v100c0%206.898%205.594%2012.5%2012.496%2012.5h37.5v37.5c0%206.898%205.598%2012.496%2012.5%2012.496h50c6.903%200%2012.5-5.598%2012.5-12.496v-37.5h249.997v37.5c0%206.898%205.593%2012.496%2012.5%2012.496h50c6.902%200%2012.5-5.598%2012.5-12.496v-37.5h37.496c6.906%200%2012.5-5.602%2012.5-12.5v-100c0-6.902-5.594-12.5-12.5-12.5h-37.496v-25h37.496c6.906%200%2012.5-5.598%2012.5-12.5v-99.996c0-6.906-5.594-12.5-12.5-12.5h-37.496v-25h37.496c6.906%200%2012.5-5.602%2012.5-12.5v-100c0-6.903-5.594-12.5-12.5-12.5H137.438c-6.903%200-12.497%205.597-12.497%2012.5v100c0%206.898%205.594%2012.5%2012.496%2012.5h37.5v25h-37.5c-6.902%200-12.496%205.594-12.496%2012.5v99.996c0%206.902%205.594%2012.5%2012.496%2012.5h37.5v25zm87.5%20150h-25v-25h25zm324.996%200h-25v-25h25zm49.996-50H149.938v-75H599.93zm-99.996-125v25H249.937v-25zm50%2025h-25v-25h25zm0-149.996h-25v-25h25zm-299.996%200v-25h249.996v25zm-100-125H599.93v75H149.938zm50%20100h25v25h-25zm-50%2050H599.93v74.996H149.938zm50%2099.996h25v25h-25zm0%200%22%2F%3E%3Cpath%20d%3D%22M549.934%20625.004h25v25h-25zm0%200M499.934%20625.004h25v25h-25zm0%200M449.934%20625.004h25v25h-25zm0%200M174.938%20625.004h25v25h-25zm0%200M672.98%20214.074c1.29-8.8%201.946-17.676%201.95-26.562.03-86.524-59.168-161.828-143.254-182.215-84.082-20.39-171.2%2019.426-210.809%2096.351-25.562-25.183-60.043-39.246-95.93-39.136-75.902.09-137.406%2061.597-137.496%20137.5%200%204.222.196%208.445.586%2012.675C37.47%20215.774-1.48%20258.462.043%20309.09c1.535%2050.625%2043%2090.879%2093.648%2090.918h6.25v-25h-6.25c-37.968%200-68.75-30.781-68.75-68.75%200-37.973%2030.782-68.746%2068.75-68.746h8.75c3.754%200%207.309-1.688%209.68-4.602%202.375-2.906%203.32-6.722%202.57-10.406-1.496-7.402-2.25-14.938-2.25-22.492-.054-48.301%2030.754-91.227%2076.52-106.633%2045.773-15.41%2096.273.14%20125.437%2038.629%202.747%203.605%207.22%205.441%2011.696%204.8%204.48-.632%208.27-3.636%209.902-7.859C364.164%2055.945%20440.383%2013.402%20517.301%2027.754c76.922%2014.348%20132.68%2081.512%20132.629%20159.758-.024%2011.773-1.32%2023.5-3.875%2034.992-.801%203.652.074%207.46%202.37%2010.398%202.305%202.934%205.802%204.692%209.532%204.786%2036.598%202.253%2064.977%2032.84%2064.5%2069.503-.473%2036.664-29.633%2066.504-66.277%2067.817h-6.25v25h6.25c48.414-.133%2088.77-37.098%2093.125-85.317%204.36-48.214-28.715-91.82-76.325-100.617zm0%200%22%2F%3E%3C%2Fsvg%3E')"
      },
      {
        name: '测试图形2',
        background_id: '002',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20height%3D%221000%22%20viewBox%3D%22-162%200%20750%20750%22%20width%3D%221000%22%3E%3Cpath%20d%3D%22M412.5%200h-400C5.594%200%200%205.594%200%2012.5v700c0%206.906%205.594%2012.5%2012.5%2012.5H50v25h25v-25h275v25h25v-25h37.5c6.906%200%2012.5-5.594%2012.5-12.5v-700C425%205.594%20419.406%200%20412.5%200zM400%20700H25V25h375zm0%200%22%2F%3E%3Cpath%20d%3D%22M62.5%20675h300c6.906%200%2012.5-5.594%2012.5-12.5v-600c0-6.906-5.594-12.5-12.5-12.5h-300C55.594%2050%2050%2055.594%2050%2062.5v600c0%206.906%205.594%2012.5%2012.5%2012.5zM350%20650H75v-75h275zm0-100H75v-75h275zm0-100H75v-75h275zm0-100H75v-75h275zm0-100H75v-75h275zm0-175v75H75V75zm0%200%22%2F%3E%3Cpath%20d%3D%22M300%20100h25v25h-25zm0%200M250%20100h25v25h-25zm0%200M80%20100h125v25H100zm0%200M300%20200h25v25h-25zm0%200M250%20200h25v25h-25zm0%200M80%20200h125v25H100zm0%200M300%20300h25v25h-25zm0%200M250%20300h25v25h-25zm0%200M80%20300h125v25H100zm0%200M300%20400h25v25h-25zm0%200M250%20400h25v25h-25zm0%200M80%20400h125v25H100zm0%200M300%20500h25v25h-25zm0%200M250%20500h25v25h-25zm0%200M80%20500h125v25H100zm0%200M300%20600h25v25h-25zm0%200M250%20600h25v25h-25zm0%200M80%20600h125v25H100zm0%200%22%2F%3E%3C%2Fsvg%3E')"
      },
      {
        name: '测试图形3',
        background_id: '003',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20512%20512%22%3E%3Cpath%20d%3D%22M130%20246c-5.52%200-10%204.48-10%2010s4.48%2010%2010%2010%2010-4.48%2010-10-4.48-10-10-10z%22%2F%3E%3Cpath%20d%3D%22M256%200C118.953%200%200%20116.932%200%20256c0%20139.219%20119.11%20256%20256%20256%20137.832%200%20256-77.678%20256-256C512%20116.777%20392.886%200%20256%200zm180.145%20106.199c33.835%2040.246%2053.341%2089.305%2055.623%20139.801H452v-30c0-16.542-13.458-30-30-30h-35.089c-3.106-20.556-7.755-40.444-13.875-59.354%2023.071-5.423%2044.221-12.281%2063.109-20.447zm-14.358-15.677c-16.714%206.729-35.566%2012.553-55.512%2017.152-13.126-33.552-30.229-60.607-49.392-79.204%2038.915%2010.951%2075.167%2032.233%20104.904%2062.052zM266%2021.077c29.768%206.334%2059.944%2040.245%2080.386%2090.711-26.063%204.787-53.471%207.546-80.386%208.099v-98.81zm0%20118.813c29.271-.578%2059.119-3.675%2087.363-9.068%205.804%2017.552%2010.26%2036.039%2013.309%2055.178H266v-46.11zM246%2021.077v98.81c-26.915-.552-54.322-3.311-80.386-8.099C186.056%2061.321%20216.232%2027.41%20246%2021.077zm0%20118.813V186H145.328c3.048-19.138%207.505-37.626%2013.309-55.177%2028.244%205.392%2058.092%208.489%2087.363%209.067zM195.118%2028.469c-19.164%2018.598-36.266%2045.653-49.392%2079.205-19.946-4.599-38.798-10.422-55.513-17.152%2029.736-29.819%2065.989-51.101%20104.905-62.053zm-79.263%2077.73c18.888%208.166%2040.039%2015.024%2063.109%2020.447-6.119%2018.91-10.769%2038.798-13.875%2059.354H90c-16.542%200-30%2013.458-30%2030v30H20.232c2.282-50.496%2021.788-99.555%2055.623-139.801zm0%20299.602C42.02%20365.555%2022.514%20316.496%2020.232%20266H60v30c0%2016.542%2013.458%2030%2030%2030h35.089c3.106%2020.556%207.755%2040.444%2013.875%2059.354-23.071%205.423-44.221%2012.281-63.109%2020.447zm14.358%2015.677c16.714-6.729%2035.567-12.553%2055.512-17.152%2013.126%2033.552%2030.229%2060.607%2049.392%2079.204-38.915-10.951-75.168-32.233-104.904-62.052zM246%20490.923c-29.768-6.334-59.944-40.245-80.386-90.711%2026.063-4.787%2053.471-7.546%2080.386-8.099v98.81zM246%20326v46.11c-29.271.578-59.119%203.675-87.363%209.068-5.804-17.552-10.26-36.039-13.309-55.178H246zM90%20306c-5.514%200-10-4.486-10-10v-80c0-5.514%204.486-10%2010-10h288.186l.021.001.015-.001H422c5.514%200%2010%204.486%2010%2010v80c0%205.514-4.486%2010-10%2010H90zm276.672%2019.9c-3.048%2019.138-7.505%2037.726-13.309%2055.277-28.244-5.392-58.092-8.489-87.363-9.067V325.9h100.672zM266%20490.923v-98.81c26.915.552%2054.322%203.311%2080.386%208.099-20.442%2050.467-50.618%2084.378-80.386%2090.711zm50.882-7.392c19.164-18.598%2036.266-45.653%2049.392-79.205%2019.946%204.599%2038.798%2010.422%2055.513%2017.152-29.736%2029.819-65.989%2051.101-104.905%2062.053zm119.263-77.73c-18.888-8.166-40.039-15.024-63.109-20.447%206.119-18.91%2010.769-38.798%2013.875-59.354H422c16.542%200%2030-13.458%2030-30v-30.1h39.768c-2.282%2050.496-21.788%2099.655-55.623%20139.901z%22%2F%3E%3Cpath%20d%3D%22M210%20246h-40c-5.522%200-10%204.477-10%2010s4.478%2010%2010%2010h40c5.522%200%2010-4.477%2010-10s-4.478-10-10-10zM302%20246h-46c-5.522%200-10%204.477-10%2010s4.478%2010%2010%2010h46c5.522%200%2010-4.477%2010-10s-4.478-10-10-10zM382%20246h-40c-5.522%200-10%204.477-10%2010s4.478%2010%2010%2010h40c5.522%200%2010-4.477%2010-10s-4.478-10-10-10z%22%2F%3E%3C%2Fsvg%3E')"
      },
      {
        name: '测试图形4',
        background_id: '004',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20512%20512%22%3E%3Cpath%20d%3D%22M150%2060c-5.52%200-10%204.48-10%2010s4.48%2010%2010%2010%2010-4.48%2010-10-4.48-10-10-10z%22%2F%3E%3Cpath%20d%3D%22M412%20320c55.141%200%20100-44.86%20100-100s-44.859-100-100-100c-8.122%200-16.319%201.08-24.483%203.218C370.215%2052.119%20301.209%200%20226%200%20148.888%200%2078.951%2054.564%2063.528%20127.319%2025.29%20142.312%200%20178.836%200%20220c0%2055.14%2044.859%2080%2080%20100h146v52H136c-16.542%200-30%2013.458-30%2030v31.266c-17.232%204.452-30%2020.13-30%2038.734%200%2022.056%2017.944%2040%2040%2040s40-17.944%2040-40c0-18.604-12.768-34.282-30-38.734V402c0-5.514%204.486-10%2010-10h110v41.266c-17.232%204.452-30%2020.13-30%2038.734%200%2022.056%2017.944%2040%2040%2040s40-17.944%2040-40c0-18.604-12.768-34.282-30-38.734V392h110c5.514%200%2010%204.486%2010%2010v31.266c-17.232%204.452-30%2020.13-30%2038.734%200%2022.056%2017.944%2040%2040%2040s40-17.944%2040-40c0-18.604-12.768-34.282-30-38.734V402c0-16.542-13.458-30-30-30H266v-52h146zM136%20472c0%2011.028-8.972%2020-20%2020s-20-8.972-20-20%208.972-20%2020-20%2020%208.972%2020%2020zm280%200c0%2011.028-8.972%2020-20%2020s-20-8.972-20-20%208.972-20%2020-20%2020%208.972%2020%2020zm-140%200c0%2011.028-8.972%2020-20%2020s-20-8.972-20-20%208.972-20%2020-20%2020%208.972%2020%2020zM80%20300c-44.112%200-80-35.888-80-80%200-34.478%2022.255-64.896%2055.379-75.692.874-.285%201.69-.683%202.434-1.178%2027.287-7.868%2057.547-.907%2078.755%2020.301%203.906%203.905%2010.236%203.905%2014.143%200%203.905-3.905%203.905-10.237%200-14.143C151.823%20130.402%20126.711%20120%2080%20120c-4.775%200-9.518.353-14.205%201.021C103.412%2063.296%20162.07%2020%20226%2020c67.408%200%20128.42%2047.679%20142.535%20109.915-10.093%204.867-19.234%2011.362-27.246%2019.374-3.905%203.905-3.905%2010.237%200%2014.142%203.905%203.904%2010.237%203.906%2014.143%200C371.128%20147.732%20392.844%20140%20412%20140c44.112%200%2080%2035.888%2080%2080s-35.888%2080-80%2080H100z%22%2F%3E%3Cpath%20d%3D%22M309.829%2068.532C289.51%2051.2%20256.604%2040%20226%2040c-7.772%200-29.905%201.704-41.897%205.444-5.272%201.645-8.213%207.251-6.569%2012.524%201.645%205.272%207.252%208.212%2012.524%206.569C199.505%2061.59%20215.627%2060%20226%2060c25.725%200%2054.197%209.544%2070.851%2023.749%204.202%203.584%2010.514%203.082%2014.098-1.119%203.583-4.202%203.082-10.514-1.12-14.098z%22%2F%3E%3C%2Fsvg%3E')"
      }
    ]
  }
  const configObj = {
    timeOutEvent: 0,
    isMouseDown: false,
    torpData: {
      nodes: [],
      links: [],
      lines: [],
      text: []
    },
    initFlag: true,
    hoverFlag: false
  }

  const getXariaYaria = (limitNum, ariaType) => {
    // console.log('limitNum', limitNum)
    // console.log('ariaType', ariaType)
    let resaultNum = limitNum
    const key = ariaType === 'X' ? 'x' : 'y'
    const arr = configObj.torpData.nodes.filter((v) => { return v[key] > limitNum })
    if (arr.length > 0) {
      const rltArr = []
      arr.forEach((v) => {
        rltArr.push(v[key])
      })
      rltArr.sort((a, b) => { return a - b })
      // console.log('rltArr', rltArr)
      resaultNum = rltArr[rltArr.length - 1] + 100
    }
    // console.log('resaultNum', resaultNum)

    return resaultNum
  }
  // 初始化组件，渲染视窗元素
  this.init = () => {
    // 提示浏览器兼容，IE11以下提示兼容信息
    if ((navigator.userAgent.toLowerCase().indexOf('trident') > -1 && navigator.userAgent.toLowerCase().indexOf('trident/7.0') < 0) || navigator.userAgent.toLowerCase().indexOf('msie') > -1) {
      alert('您的浏览器版本过低，或不兼容本组件，请尝试使用新版chrome浏览器或火狐浏览器浏览～')
    }

    // 根据左中右视窗是否设置显示计算最后显示的视窗比例
    const _self = this
    const leftViewWidth = configObj.leftViewShow && configObj.couldEdit ? configObj.leftViewWidth : 0
    const centerViewWidth = configObj.centerViewShow ? configObj.centerViewWidth : 0
    const rightViewWidth = configObj.rightViewShow && configObj.couldEdit ? configObj.rightViewWidth : 0
    const widthAdd = computeViewWidth(leftViewWidth, centerViewWidth, rightViewWidth)
    const leftDiv = $('<div>').addClass('l000_view l000_left000_view').css({ 'width': (configObj.leftViewShow && configObj.couldEdit ? (leftViewWidth + widthAdd) / 24 * 100 : 0) + '%' }).hide().appendTo('#' + configObj.mainBoxId)
    const centerDiv = $('<div>').addClass('l000_view l000_opera000_view').css({ 'width': (configObj.centerViewWidth + widthAdd) / 24 * 100 + '%' }).appendTo('#' + configObj.mainBoxId)
    const canvasDft = $('<canvas width="' + getXariaYaria(centerDiv.outerWidth(), 'X') + '" height="' + getXariaYaria(centerDiv.outerHeight(), 'Y') + '">').attr('id', configObj.canvasId).appendTo(centerDiv)
    const rightDiv = $('<div>').addClass('l000_view l000_right000_view').css({ 'width': (configObj.rightViewShow && configObj.couldEdit ? (rightViewWidth + widthAdd) / 24 * 100 : 0) + '%' }).hide().appendTo('#' + configObj.mainBoxId)
    const infoWindow = $('<div data-id=""></div>').addClass('l000_torp000_info000_window').appendTo(centerDiv)
    if (configObj.couldEdit) {
      // const inputButtonlabel = $('<button class="l000_inputButton">导入</button>').appendTo(centerDiv)
      const inputButton = $('<input type="file" id="l000_inputButton" style="opacity: 0;">').on('change', function() { handleFiles($(this)[0].files[0]) }).appendTo(centerDiv)
      const outputButton = $('<button id="l000_outputButton">导出</button>').on('click', () => { saveJSON(this.getTorpData(), false) }).appendTo(centerDiv)
      const innerLeft = new Promise((resolve, reject) => {
        if (configObj.leftViewShow) { leftDiv.show(); resolve() } else { leftDiv.hide() }
      }).then(() => {
        innerLeftView()
      })
      const innerRight = new Promise((resolve, reject) => {
        if (configObj.rightViewShow) { rightDiv.show(); resolve(this) } else { rightDiv.hide() }
      }).then(() => {
        innerRightView()
      })
    }
    if (configObj.onlyDrag) {
      // const saveButton = $('<button id="l000_outputButton">保存</button>').on('click', () => { saveJSON(this.getTorpData(), true) }).appendTo(centerDiv)
    }
    const innerCenter = new Promise((resolve, reject) => {
      if (configObj.centerViewShow) { centerDiv.show(); resolve(this) } else { centerDiv.hide() }
    }).then((_this) => {
      $('.l000_opera000_view').on('mousemove', function(e) {
        $('.l000_torp000_info000_window').css(JSON.parse(computInfoWindowPosition(e)))
      })
      $('#' + configObj.canvasId).on('mousemove', (e) => {
        if ($('.l000_left000_active').length > 0 && $('.l000_left000_active').attr('data-type') === 'text') {
          $('#' + configObj.canvasId).css('cursor', 'text')
        } else {
          $('#' + configObj.canvasId).css('cursor', 'unset')
        }
        refreshCanvas($('#' + configObj.canvasId), e, false)
        if (configObj.hoverFlag) {
          if (configObj.onlyDrag) {
            $('#' + configObj.canvasId).addClass('l000_pointer')
          } else {
            $('.l000_torp000_info000_window').show()
          }
          configObj.hoverFlag = false
        } else {
          if (configObj.onlyDrag) {
            $('#' + configObj.canvasId).removeClass('l000_pointer')
          } else {
            $('.l000_torp000_info000_window').hide()
          }
        }
        // $('.l000_torp000_info000_window').css(JSON.parse(computInfoWindowPosition(e)))
      })
      $('#' + configObj.canvasId).off('mouseup').on('mouseup', (e) => {
        if ($('.l000_left000_active').length > 0) {
          const xNum = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true))
          const yNum = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top)
          let left = xNum
          let top = yNum
          left += $('.l000_opera000_view').scrollLeft()
          top += $('.l000_opera000_view').scrollTop()
          if ($('.l000_left000_active').attr('data-type') === 'text') {
            const id = new Date().getTime()
            const box = $('<div>').addClass('l000_torp000_element l000_left000_text').prop('id', 'l000_torp000_text000_' + id).css({ 'top': top, 'left': left }).appendTo('.l000_opera000_view')
            const div = $('<div><span class="l000_text000_close">+</span><p class="l000_text000_area">自定义文本</p><input class="l000_text000_input" type="text" value="自定义文本"></div>').appendTo(box)
            configObj.torpData.text.push({ id: 'l000_torp000_text000_' + id, x: left, y: top, textValue: '自定义文本' })
            div.find('.l000_text000_close').on('click', function(e) {
              e.stopPropagation()
              const resaultArr = []
              configObj.torpData.text.forEach((v) => {
                if (v.id !== $(this).parents('.l000_left000_text').prop('id')) {
                  resaultArr.push(v)
                }
              })
              configObj.torpData.text = resaultArr
              $(this).parents('.l000_left000_text').remove()
            })
            div.find('.l000_text000_area').on('click', function(e) {
              e.stopPropagation()
              $(this).hide().siblings('input').show()
            })
            div.find('.l000_text000_input').on('input', function(e) {
              e.stopPropagation()
              $(this).siblings('p').text($(this).val())
            }).on('blur', function(e) {
              e.stopPropagation()
              e.preventDefault()
              if ($(this).val()) {
                configObj.torpData.text.forEach((v) => {
                  if (v.id === $(this).parents('.l000_left000_text').prop('id')) {
                    v.textValue = $(this).val()
                  }
                })
                $(this).hide().siblings('p').show()
              } else {
                const resaultArr = []
                configObj.torpData.text.forEach((v) => {
                  if (v.id !== $(this).parents('.l000_left000_text').prop('id')) {
                    resaultArr.push(v)
                  }
                })
                configObj.torpData.text = resaultArr
              }
            })
            div.hover(function() {
              $(this).css('background', 'rgba(83,173,255,0.6)').find('.l000_text000_close').show()
            }, function() {
              $(this).css('background', 'none').find('.l000_text000_close').hide()
            })
            changeBind(div)
            $('#' + configObj.canvasId).css('cursor', 'text')
            $('.l000_left000_active').removeClass('l000_left000_active')
          } else {
            if ($('.l000_left000_active').attr('data-type') === 'linear') {
              if (configObj.torpData.lines.length === 0 || configObj.torpData.lines[configObj.torpData.lines.length - 1].end) {
                configObj.torpData.lines.push({ id: 'l000_lines000_' + new Date().getTime(), start: { x: left, y: top }, end: null })
              } else if (configObj.torpData.lines[configObj.torpData.lines.length - 1].end === null) {
                if (Math.abs(left - configObj.torpData.lines[configObj.torpData.lines.length - 1].start.x) > Math.abs(top - configObj.torpData.lines[configObj.torpData.lines.length - 1].start.y)) {
                  top = configObj.torpData.lines[configObj.torpData.lines.length - 1].start.y
                } else {
                  left = configObj.torpData.lines[configObj.torpData.lines.length - 1].start.x
                }
                configObj.torpData.lines[configObj.torpData.lines.length - 1].end = { x: left, y: top }
              }
            } else {
              $('.l000_left000_active').removeClass('l000_left000_active')
            }
            $('#' + configObj.canvasId).css('cursor', 'unset')
          }
        }
        refreshCanvas($('#' + configObj.canvasId), e, true)
      })
    })
  }
  // 根据当前显示的视窗，计算隐藏的视窗多余宽度应分配给其它显示视窗多少比例
  const computeViewWidth = (l, c, r) => {
    let countNum = 0
    if (configObj.leftViewShow && configObj.couldEdit) countNum++
    if (configObj.centerViewShow) countNum++
    if (configObj.rightViewShow && configObj.couldEdit) countNum++
    return (24 - l - c - r) / countNum
  }
  // 合并配置项的方法
  const mergeObjectKey = (paramObj, baseObj) => {
    Object.keys(baseObj).forEach((v) => {
      if (paramObj[v] !== undefined && paramObj[v] !== null && Object.prototype.toString.call(baseObj[v]) === Object.prototype.toString.call(paramObj[v])) {
        configObj[v] = paramObj[v]
      } else {
        configObj[v] = baseObj[v]
      }
    })
  }
  // 渲染左侧视窗数据
  const innerLeftView = () => {
    $('.l000_left000_view').empty()
    const _self = this
    const elementul = $('<div class="l000_left000_drag000_box">' +
            '<h5 class="l000_title l000_open">拖拽元素</h5>' +
            '</div>').addClass('l000_form000_ul').appendTo('.l000_left000_view')
    const elementul2 = $('<div class="l000_left000_drag000_box">' +
            '<h5 class="l000_title l000_open">工具箱</h5>' +
            '<div class="l000_tool000_btn" data-type="linear">—</div>' +
            '<div class="l000_tool000_btn" data-type="text">T</div>' +
            '</div>').addClass('l000_form000_ul').appendTo('.l000_left000_view')
    configObj.elementType.forEach((v, i) => {
      const div = $('<div draggable="true"><p>' + v.name + '</p></div>').attr({ 'id': 'l000_drag000_id000_' + (i + 1), 'data-name': v.name, 'data-background-id': v.background000_id }).addClass('l000_drag000_able l000_drag000_element').css({ 'background': v.svg + ' #fff center no-repeat', 'background-size': '90% 90%' }).appendTo(elementul)
      addDragEvent(div)
    })
    addDropEvent($('.l000_opera000_view'))
    /*$('.l000_tool000_btn').off('click').on('click', function(e) {
      if ($(this).hasClass('l000_left000_active')) {
        handleToolBtn(null, $(this).attr('data-type'))
        $(this).removeClass('l000_left000_active')
      } else {
        if ($('.l000_left000_active').length > 0) {
          handleToolBtn($(this).attr('data-type'), $('.l000_left000_active').attr('data-type'))
        } else {
          handleToolBtn($(this).attr('data-type'), null)
        }
        $('.l000_left000_active').removeClass('l000_left000_active')
        $(this).addClass('l000_left000_active')
      }
      if ($('.l000_left000_active').length === 0) {
        if (configObj.torpData.lines[configObj.torpData.lines.length - 1].end === null) {
          configObj.torpData.lines.pop()
          refreshCanvas($('#' + configObj.canvasId), e, false)
        }
      }
    })*/
  }
  // 处理工具栏点击事件方法
  const handleToolBtn = (clickEl, prevEl) => {
    // console.log(clickEl,prevEl)
    // if(clickEl){
    //     this['#start_'+clickEl]();
    // }
    // if(prevEl){
    //     this['#end_'+clickEl]();
    // }
  }
  // 渲染右侧视窗数据
  const innerRightView = () => {
    $('.l000_right000_view').empty()
    // 元素属性框初始化渲染及表单事件绑定
    const _self = this
    const elementBox = $('<div>').addClass('l000_element000_box l000_right000_box').hide().appendTo($('.l000_right000_view'))
    const elementul = $('<ul>' +
            '<h5 class="l000_title l000_open">基础属性</h5>' +
            '<li><label>元素名称：<input class="l000_element000_name" type="text" placeholder="请输入元素名称"></label></li>' +
            '<li><label>自定义ID：<input class="l000_element000_id" type="text" placeholder="请输入元素ID"></label></li>' +
            '<li><label>元素样式：<select class="l000_element000_style"><option value="-1">自定义样式</option></select></label></li>' +
            '<li class="l000_diy000_style"><label>自定义样式：</label><div><p>预览效果</p><span id="img_view"></span><input id="l000_img000_file" type="file"><b>选择文件</b></div></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(elementBox)
    configObj.elementType.forEach((v) => {
      const option = $('<option>').val(v.background_id).text(v.name)
      elementul.find('select.l000_element000_style').append(option)
    })
    elementul.find('input.l000_element000_name').off('input').on('input', function() {
      if ($('.l000_element000_box').attr('data-element-id')) {
        $('#' + $('.l000_element000_box').attr('data-element-id')).attr('data-name', $(this).val()).find('p').text($(this).val())
      }
    }).off('blur').on('blur', function() {
      const val = $(this).val()
      configObj.torpData.nodes.forEach((v) => {
        if (v.id === $('.l000_element000_box').attr('data-element-id')) {
          v.name = val
        }
      })
    })
    const elementul2 = $('<ul>' +
            '<h5 class="l000_title l000_open">自定义属性</h5>' +
            '<ul>参数格式：<br>{' +
            '<li class="l000_nomargin"> ' +
            '<p>“<span class="l000_key"></span>”:”<span class="l000_value"></span>”,</p>' +
            '</li>}' +
            '<li>html自定属性格式：<br> ' +
            '<p>data-torp-<span class="l000_data000_attr000_key"></span>=“<span class="l000_data000_attr000_value"></span>”</p>' +
            '</li>' +
            '</ul><br>' +
            '<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值"><span class="l000_delete000_diy000_style">+</span></li>' +
            '<li class="l000_add000_diy000_style"><p>新增自定义属性</p></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(elementBox)

    const lineBox = $('<div>').addClass('l000_line000_box l000_right000_box').hide().appendTo($('.l000_right000_view'))
    const lineul = $('<ul>' +
            '<h5 class="l000_title l000_open">基础属性</h5>' +
            '<li><label>线条ID：<input class="l000_line000_id" type="text" placeholder="请输入线条ID"></label></li>' +
            '<li><label>线条名称：<input class="l000_line000_name" type="text" placeholder="请输入线条名称"></label></li>' +
            '<li><label>线条样式：<select class="l000_line000_style"><option value="line">实线</option><option value="dash">虚线</option></select></label></li>' +
            '<li><label>箭头样式：<select class="l000_arrow000_style"><option value="single">单向箭头</option><option value="both">双向箭头</option><option value="none">无箭头</option></select></label></li>' +
            '<li><label>线条颜色：<select class="l000_line000_color"><option value="#53ADFF">#53ADFF</option><option value="#FF5D54">#FF5D54</option><option value="#17E572">#17E572</option><option value="-1">自定义颜色</option></select></label></li>' +
            '<li class="l000_diy000_color"><label>自定义颜色：</label><div><span id="l000_color"></span><input id="l000_color000_input" type="text" placeholder="请输入十六进制色码"></div></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(lineBox)
    elementul.find('select.l000_element000_style').empty()
    elementul.find('select.l000_element000_style').append($('<option value="-1">自定义样式</option>'))
    configObj.elementType.forEach((v) => {
      const option = $('<option>').val(v.background_id).text(v.name)
      elementul.find('select.l000_element000_style').append(option)
    })
    const lineul2 = $('<ul>' +
            '<h5 class="l000_title l000_open">自定义属性</h5>' +
            '<ul>参数格式：<br>{' +
            '<li class="l000_nomargin"> ' +
            '<p>“<span class="l000_key"></span>”:”<span class="l000_value"></span>”,</p>' +
            '</li>}' +
            '<li>html自定属性格式：<br> ' +
            '<p>data-torp-<span class="l000_data000_attr000_key"></span>=“<span class="l000_data000_attr000_value"></span>”</p>' +
            '</li>' +
            '</ul><br>' +
            '<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值"><span class="l000_delete000_diy000_style">+</span></li>' +
            '<li class="l000_add000_diy000_style"><p>新增自定义属性</p></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(lineBox)

    elementul2.find('input').on('input', function() {
      const liIdx = $(this).parent().index() - 3
      const iptIdx = $(this).index()
      const val = $(this).val()
      $(this).parents('ul.l000_form000_ul').find('li').each(function() {
        $(this).find('p').each(function(i) {
          if (i === liIdx) {
            $(this).find('span').eq(iptIdx).text(val)
          }
        })
      })
    }).on('blur', function(e) {
      e.preventDefault()
      if ($(this).parent().find('input').eq(0).val() == '') {
        $(this).parent().find('input').eq(0).val('diy000_attr000_' + new Date().getTime())
      } else {
        const idx = $(this).parent().index() - 3
        const val = $(this).parent().find('input').eq(0).val()
        let flag = true
        elementul2.find('li.l000_diy000_input000_box').each(function(i) {
          if (i !== idx && $(this).find('input').eq(0).val() === val) {
            flag = false
          }
        })
        if (flag) {
          updateDiyAttr('data-element-id', 'nodes', elementul2)
        } else {
          alert('自定义属性名不可以重复！')
          $(this).parent().find('input').eq(0).val('')
          const val2 = $(this).parent().find('input').eq(1).val()
          const idx = $(this).parent().index() - 3
          $(this).parent().siblings('ul').find('li').each(function() {
            $(this).find('p').each(function(i) {
              if (i === idx) {
                $(this).find('span').eq(0).text('')
                $(this).find('span').eq(1).text(val2)
              }
            })
          })
        }
      }
    })
    lineul2.find('input').on('input', function() {
      const liIdx = $(this).parent().index() - 3
      const iptIdx = $(this).index()
      const val = $(this).val()
      $(this).parents('ul.l000_form000_ul').find('li').each(function() {
        $(this).find('p').each(function(i) {
          if (i === liIdx) {
            $(this).find('span').eq(iptIdx).text(val)
          }
        })
      })
    }).on('blur', function(e) {
      e.preventDefault()
      if ($(this).parent().find('input').eq(0).val() == '') {
        $(this).parent().find('input').eq(0).val('diy000_attr000_' + new Date().getTime())
      } else {
        const idx = $(this).parent().index() - 3
        const val = $(this).parent().find('input').eq(0).val()
        let flag = true
        lineul2.find('li.l000_diy000_input000_box').each(function(i) {
          if (i !== idx && $(this).find('input').eq(0).val() === val) {
            flag = false
          }
        })
        if (flag) {
          updateDiyAttr('data-line-id', 'links', lineul2)
        } else {
          alert('自定义属性名不可以重复！')
          $(this).parent().find('input').eq(0).val('')
          const val2 = $(this).parent().find('input').eq(1).val()
          const idx = $(this).parent().index() - 3
          $(this).parent().siblings('ul').find('li').each(function() {
            $(this).find('p').each(function(i) {
              if (i === idx) {
                $(this).find('span').eq(0).text('')
                $(this).find('span').eq(1).text(val2)
              }
            })
          })
        }
      }
    })
    elementul2.find('.l000_delete000_diy000_style').on('click', function(e) {
      e.stopPropagation()
      e.preventDefault()
      if (elementul2.find('.l000_delete000_diy000_style').length < 2) {
        $(this).parent().find('input').eq(0).val('')
        $(this).parent().find('input').eq(1).val('')
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).find('span').eq(0).text('')
              $(this).find('span').eq(1).text('')
            }
          })
        })
      } else {
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).remove()
            }
          })
        })
        $(this).parent().remove()
      }
      updateDiyAttr('data-element-id', 'nodes', elementul2)
    })
    lineul2.find('.l000_delete000_diy000_style').on('click', function(e) {
      e.stopPropagation()
      e.preventDefault()
      if (lineul2.find('.l000_delete000_diy000_style').length < 2) {
        $(this).parent().find('input').eq(0).val('')
        $(this).parent().find('input').eq(1).val('')
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).find('span').eq(0).text('')
              $(this).find('span').eq(1).text('')
            }
          })
        })
      } else {
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).remove()
            }
          })
        })
        $(this).parent().remove()
      }
      updateDiyAttr('data-line-id', 'links', lineul2)
    })
    $('.l000_element000_id').on('blur', function() {
      if ($(this).val() == '') {
        $(this).val('l000_torp000_' + new Date().getTime())
      }
      if ($(this).val() !== $(this).attr('data-old-id') && $('#' + $(this).val()).length === 0) {
        $('#' + $(this).attr('data-old-id')).prop('id', $(this).val())
        $('.l000_element000_box').attr('data-element-id', $(this).val())
        configObj.torpData.nodes.forEach((v) => {
          if (v.id === $(this).attr('data-old-id')) {
            v.id = $(this).val()
          }
        })
      } else {
        if ($('#' + $(this).val()).length > 0) {
          alert('自定义ID重复！')
          $(this).val('')
        }
      }
    })
    $('.l000_element000_name').on('blur', function() {
      configObj.torpData.nodes.forEach((v) => {
        if (v.id === $('.l000_element000_box').attr('data-element-id')) {
          v.name = $(this).val()
        }
      })
    })
    $('.l000_line000_name').on('blur', function() {
      configObj.torpData.links.forEach((v) => {
        if (v.id === $('.l000_line000_box').attr('data-line-id')) {
          v.name = $(this).val()
        }
      })
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    })
    $('#l000_color000_input').on('blur', function() {
      configObj.torpData.links.forEach((v) => {
        if (v.id === $('.l000_line000_box').attr('data-line-id')) {
          v.color = '#' + $(this).val()
          $('#l000_color').css('background', '#' + $(this).val())
        }
      })
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    })
    $('.l000_line000_id').on('blur', function() {
      let flag = true
      if ($(this).val() == '') {
        $(this).val('l000_line000_' + new Date().getTime())
      }
      configObj.torpData.links.forEach(function(v) {
        if ($(this).val() === v.id) {
          flag = false
        }
      })
      if ($(this).val() !== $(this).attr('data-old-id') && flag) {
        $('.l000_line000_box').attr('data-line-id', $(this).val())
        configObj.torpData.links.forEach((v) => {
          if (v.id === $(this).attr('data-old-id')) {
            v.id = $(this).val()
          }
        })
      } else {
        if (!flag) {
          alert('自定义ID重复！')
          $(this).val('')
        }
      }
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    })
    elementul.find('select.l000_element000_style').on('change', () => {
      if (elementBox.attr('data-element-id')) {
        if (elementul.find('select.l000_element000_style').val() == -1) {
          $('.l000_diy000_style').show()
        } else {
          $('.l000_diy000_style').hide()
          $('#l000_img000_file').val('')
          $('#img000_view').css('background', '#ccc')
        }
        configObj.torpData.nodes.forEach((v) => {
          if (v.id === $('.l000_element000_box').attr('data-element-id')) {
            v.background_id = $('.l000_element000_style').val()
            configObj.elementType.forEach((j) => {
              if (j.background_id === $('.l000_element000_style').val()) {
                v.background = j.svg
                $('#' + $('.l000_element000_box').attr('data-element-id')).attr('data-background-id', $('.l000_element000_style').val()).css({ 'background': j.svg + ' center no-repeat ', 'background-size': '90% 90%' })
              }
            })
          }
        })
      }
    })
    lineul.find('select.l000_line000_color').on('change', () => {
      if (lineBox.attr('data-line-id')) {
        if (lineul.find('select.l000_line000_color').val() == -1) {
          $('.l000_diy000_color').show()
        } else {
          $('.l000_diy000_color').hide()
          $('#l000_color000_input').val('')
          $('#l000_color').css('background', '#ccc')
        }
        configObj.torpData.links.forEach((v) => {
          if (v.id === $('.l000_line000_box').attr('data-line-id')) {
            if (lineul.find('select.l000_line000_color').val() == -1) {
              v.color = '#' + $('#l000_color000_input').val()
            } else {
              v.color = $('.l000_line000_color').val()
            }
          }
        })
        refreshCanvas($('#' + configObj.canvasId), undefined, false)
      }
    })
    lineul.find('select.l000_line000_style').on('change', () => {
      if (lineBox.attr('data-line-id')) {
        configObj.torpData.links.forEach((v) => {
          if (v.id === $('.l000_line000_box').attr('data-line-id')) {
            v.isDash = lineul.find('select.l000_line000_style').val() === 'dash'
          }
        })
        refreshCanvas($('#' + configObj.canvasId), undefined, false)
      }
    })
    lineul.find('select.l000_arrow000_style').on('change', () => {
      if (lineBox.attr('data-line-id')) {
        configObj.torpData.links.forEach((v) => {
          if (v.id === $('.l000_line000_box').attr('data-line-id')) {
            v.arrowType = lineul.find('select.l000_arrow000_style').val()
          }
        })
        refreshCanvas($('#' + configObj.canvasId), undefined, false)
      }
    })
    $('#l000_img000_file').on('change', () => {
      const fileType = $('#l000_img000_file').val().split('.')[$('#l000_img000_file').val().split('.').length - 1]
      if (fileType.toLowerCase() === 'png' || fileType.toLowerCase() === 'jpg' || fileType.toLowerCase() === 'jpeg') {
        var file = $('#l000_img000_file')[0].files[0]
        if (file.size / 1024 < 150) {
          var reader = new FileReader()
          reader.readAsDataURL(file) // 将文件读取为Data URL小文件   这里的小文件通常是指图像与 html 等格式的文件
          reader.onload = function(e) {
            $('#img_view').css({ 'background': 'url(' + e.target.result + ') center no-repeat ', 'background-size': '90% 90%' })
            // document.getElementById("img_z_base64").value = reader.result;
            $('#' + $('.l000_element000_box').attr('data-element-id')).attr('data-background-id', $('.l000_element000_style').val()).css({ 'background': 'url(' + e.target.result + ') center no-repeat ', 'background-size': '90% 90%' })
            configObj.torpData.nodes.forEach((v) => {
              if (v.id === $('.l000_element000_box').attr('data-element-id')) {
                v.background_id = '-1'
                v.background = 'url(' + e.target.result + ')'
              }
            })
          }
        } else {
          $('#l000_img000_file').val('')
          alert('请确保图片大小在150Kb以下')
        }
      } else {
        alert('请使用png或jpg格式文件上传')
      }
    })
    elementul2.find('.l000_add000_diy000_style').on('click', function(e) {
      const p1 = $(this).siblings('ul').find('li').eq(0).find('p').eq(0).clone(true)
      const p2 = $(this).siblings('ul').find('li').eq(1).find('p').eq(0).clone(true)
      const li = $(this).siblings('li.l000_diy000_input000_box').eq(0).clone(true)
      li.find('input').val('')
      p1.find('span').text('')
      p2.find('span').text('')
      p1.appendTo($(this).siblings('ul').find('li').eq(0))
      p2.appendTo($(this).siblings('ul').find('li').eq(1))
      $(this).before(li)
    })
    lineul2.find('.l000_add000_diy000_style').on('click', function(e) {
      const p1 = $(this).siblings('ul').find('li').eq(0).find('p').eq(0).clone(true)
      const p2 = $(this).siblings('ul').find('li').eq(1).find('p').eq(0).clone(true)
      const li = $(this).siblings('li.l000_diy000_input000_box').eq(0).clone(true)
      li.find('input').val('')
      p1.find('span').text('')
      p2.find('span').text('')
      p1.appendTo($(this).siblings('ul').find('li').eq(0))
      p2.appendTo($(this).siblings('ul').find('li').eq(1))
      $(this).before(li)
    })
    elementul.find('select.l000_element000_style').find('option').eq(0).appendTo(elementul.find('select.l000_element000_style'))
    elementul.find('select.l000_element000_style').val(elementul.find('select.l000_element000_style').find('option').eq(0).val()).change()

    // 线条属性框初始化渲染及表单事件绑定
    $('.l000_title').on('mouseup', function(e) {
      e.stopPropagation()
      e.preventDefault()
      if ($(this).hasClass('l000_open')) {
        $(this).parent().css('height', '1px')
      } else {
        $(this).parent().css('height', 'auto')
      }
      $(this).toggleClass('l000_open')
    })
  }
  // 添加拖拽事件监听
  const addDragEvent = (dragElement) => {
    dragElement.off('dragstart').on('dragstart', (e) => {
      e.dataTransfer = e.originalEvent.dataTransfer
      e.dataTransfer.setData('id', e.target.id)
      e.dataTransfer.setDragImage(e.target, 30, 30)
    })
  }
  // 添加拖拽事件监听
  const addDropEvent = (dropBox) => {
    dropBox.off('dragenter').on('dragenter', (e) => {
      e.preventDefault()
    })
    dropBox.off('dragover').on('dragover', (e) => {
      e.preventDefault()
      // drop.innerHTML = '';
    })
    dropBox.off('dragleave').on('dragleave', (e) => {
      e.preventDefault()
    })
    dropBox.off('drop').on('drop', (e) => {
      e.dataTransfer = e.originalEvent.dataTransfer || window.event.dataTransfer
      const targetId = e.dataTransfer.getData('id')
      const xNum = e.originalEvent.pageX - ($('#' + targetId).parent().offset().left + $('#' + targetId).parent().outerWidth(true) + 30);
      const yNum = e.originalEvent.pageY - ($('#' + targetId).parent().offset().top + 30);
      const left = xNum > 0 ? Math.floor(xNum) : 0
      const top = xNum > 0 ? Math.floor(yNum) : 0
      if ($('#' + targetId).hasClass('l000_drag000_able')) {
        const positionObj = computPosition({ left: left, top: top }, 10, undefined)
        const elBox = $('<div>').addClass('l000_torp000_element').css({ 'top': positionObj.top, 'left': positionObj.left }).appendTo(dropBox)
        const closeBtn = $('<div>+</div>').addClass('l000_del000_torp').appendTo(elBox)
        const id = 'l000_torp000_' + new Date().getTime()
        const background = 'url(' + $('#' + targetId).prop('style')['background'].split('url(')[1].split(')')[0] + ')'
        const div = $('#' + targetId).clone(true).prop({ 'id': id, 'draggable': false }).removeClass('l000_drag000_able').appendTo(elBox)
        configObj.torpData.nodes.push(
          {
            id: id,
            x: positionObj.left,
            y: positionObj.top,
            name: div.attr('data-name'),
            background_id: div.attr('data-background-id'),
            background: background,
            diy_attr: {}
          }
        )

        // 添加连线锚点方法
        addPoint(elBox)
        // 改变clone元素的绑定事件方法
        changeBind(div)
        closeBtn.on('click', (e) => {
          if (confirm('确认删除此元素吗？')) {
            $('.l000_right000_box').hide()
            $('#l000_img000_file').val('')
            $('#img000_view').css('background', '#ccc')

            elBox.remove()
            const afterDeleteNodeArr = []
            configObj.torpData.nodes.forEach((v) => {
              if (v.id !== div.prop('id')) {
                afterDeleteNodeArr.push(v)
              }
            })
            configObj.torpData.nodes = afterDeleteNodeArr
            const afterDeletePositionArr = []
            configObj.torpData.links.forEach((v) => {
              if (v.source.indexOf(div.prop('id').split('000_')[2]) < 0 && v.target.indexOf(div.prop('id').split('000_')[2]) < 0) {
                afterDeletePositionArr.push(v)
              }
            })
            configObj.torpData.links = afterDeletePositionArr
            refreshCanvas($('#' + configObj.canvasId), e, false)
          }
        })
      }
    })
  }
  // 对于已经生成的拓扑图元素转换绑定事件
  const changeBind = (element) => {
    // 解除绑定拖拽相关事件
    element.off('dragstart,drag,dragenter,dragover,dragleave,drop')
    element.parent().off('mousedown').on('mousedown', (e) => {
      e.stopPropagation()
      // e.preventDefault();
      configObj.isMouseDown = true
      configObj.timeOutEvent = setTimeout(() => { longPress() }, 500)
      element.parent().off('mousemove').on('mousemove', (e) => {
        e.stopPropagation()
        e.preventDefault()
        // 确保本次触发的mouseMove事件是通过当前元素的mouseDown触发的，以区分hover。
        if (configObj.isMouseDown) {
          // 因为统一用mouse事件操作，因此需要将timeOutEvent归零，用于区别用户的click和drag行为。
          clearTimeout(configObj.timeOutEvent)
          configObj.timeOutEvent = 0

          // 计算当前拖拽元素位置（包含已经出现的滚动条位移）
          let xNum = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true) + 50)
          let yNum = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top + 50)
          if ($(e.target).parents('.l000_torp000_element').hasClass('l000_left000_text')) {
            xNum -= 10
            yNum -= 10
          }
          let left = xNum
          let top = yNum
          left += $('.l000_opera000_view').scrollLeft()
          top += $('.l000_opera000_view').scrollTop()

          // 元素根据鼠标光标进行相应移动
          element.parent().css({ 'left': left, 'top': top })

          // 拖拽到操作区域右边缘和下边缘时，自动增加可拖拽区域面积(和canvas画布的height和width属性，确保canvas画布不变形)并将滚动条移动至相应区域
          const topLimit = $('#' + configObj.canvasId).outerHeight(true) - e.pageY + $('.l000_opera000_view').offset().top - $('.l000_opera000_view').scrollTop()
          const leftLimit = $('#' + configObj.canvasId).outerWidth(true) - e.pageX + $('.l000_opera000_view').offset().left - $('.l000_opera000_view').scrollLeft()
          if (topLimit < 30) {
            $('#' + configObj.canvasId).prop('height', $('#' + configObj.canvasId).outerHeight(true) + 10)
            $('.l000_opera000_view').scrollTop($('.l000_opera000_view').scrollTop() + 10)
          }
          if (leftLimit < 30) {
            $('#' + configObj.canvasId).prop('width', $('#' + configObj.canvasId).outerWidth(true) + 10)
            $('.l000_opera000_view').scrollLeft($('.l000_opera000_view').scrollLeft() + 10)
          }
          refreshCanvas($('#' + configObj.canvasId), e, false)
        }
      })
    }).off('mouseup').on('mouseup', (e) => {
      e.stopPropagation()
      e.preventDefault()
      configObj.isMouseDown = false
      element.parent().off('mousemove')
      clearTimeout(configObj.timeOutEvent)
      // 根据timeOutEvent判断是否为点击事件
      if (configObj.timeOutEvent != 0) {
        // 如果点击的是图标元素，则触发显示元素属性操作区功能
        if ($(e.target).prop('class').indexOf('l000_drag000_element') > -1) {
          $('.l000_element000_checked').removeClass('l000_element000_checked')
          $(e.target).addClass('l000_element000_checked')
          init_element_form('nodes', $(e.target))
          if (configObj.onlyDrag) {
            $('.l000_mask').fadeIn()
          }
        }
        // 如果点击的是锚点，则触发连线功能
        if ($(e.target).prop('class').indexOf('l000_torp000_dot') > -1) {
          link_line($('#' + configObj.canvasId), $(e.target))
        }
      } else {
        const positionObj = computPosition({ left: parseFloat($(e.target).parent().css('left').replace('px', '')), top: parseFloat($(e.target).parent().css('top').replace('px', '')) }, 10, $(e.target).parent())
        const left = positionObj.left
        const top = positionObj.top
        $(e.target).parent().css({ 'top': top, 'left': left })
        refreshCanvas($('#' + configObj.canvasId), e, false)
      }
    }).hover(() => {
      // element.parent().find('div.l000_del000_torp').show();
      // configObj.torpData.nodes.forEach((v)=>{
      //     if(v.id === element.prop('id')){
      //         $('.l000_torp000_info000_window').attr('data-id',v.id).empty();
      //         $('<p>元素ID：'+v.id+'</p>').appendTo('.l000_torp000_info000_window');
      //         $('<p>元素名称：'+v.name+'</p>').appendTo('.l000_torp000_info000_window');
      //         if(Object.keys(v.diy000_attr).length > 0){
      //             $('<p>自定义属性：{</p>').appendTo('.l000_torp000_info000_window');
      //             Object.keys(v.diy000_attr).forEach((j)=>{
      //                 $('<p style="text-indent: 20px;">'+j+':'+v.diy000_attr[j]+',</p>').appendTo('.l000_torp000_info000_window');
      //             });
      //             $('<p>}</p>').appendTo('.l000_torp000_info000_window');

      //         }
      //         $('.l000_torp000_info000_window').show();
      //     }
      // });
    }, () => {
      element.parent().find('div.l000_del000_torp').hide()
      $('.l000_torp000_info000_window').hide()
    })
  }
  // 计算连线方法
  const link_line = (canvasElement, targetElement) => {
    const dragId = targetElement.parent().find('div.l000_drag000_element').prop('id').split('l000_torp000_')[1]
    if (targetElement.hasClass('l000_dot000_active')) {
      configObj.torpData.links.pop()
      targetElement.removeClass('l000_dot000_active')
    } else {
      targetElement.addClass('l000_dot000_active')
    }
    if ($('.l000_dot000_active').length === 1) {
      const sourceClass = 'l000_' + targetElement.attr('data-position') + '000_' + dragId + '000_' + new Date().getTime()
      targetElement.addClass(sourceClass)
      configObj.torpData.links.push({ id: 'l000_line000_' + new Date().getTime(), name: '', source: sourceClass, target: null, color: '#53ADFF', isDash: false, arrowType: 'single', diy_attr: {}})
    }
    if ($('.l000_dot000_active').length === 2) {
      const targetClass = 'l000_' + targetElement.attr('data-position') + '000_' + dragId + '000_' + new Date().getTime()
      targetElement.addClass(targetClass)
      // 判断是否有重复连线
      if (hasLine(dragId)) {
        const sourceClass = configObj.torpData.links[configObj.torpData.links.length - 1]['source']
        alert('已有连线关系，请勿重复连线')
        targetElement.removeClass(targetClass)
        $('.' + sourceClass).removeClass(sourceClass)
        configObj.torpData.links.pop()
      } else {
        configObj.torpData.links[configObj.torpData.links.length - 1]['target'] = targetClass
      }
      // 连线完成，删除锚点选中样式
      $('.l000_dot000_active').removeClass('l000_dot000_active')
    }
  }
  // 刷新canvas画布方法
  const refreshCanvas = (element, e, ischeckClick) => {
    const canvas = element[0]
    const context = canvas.getContext('2d')
    context.clearRect(0, 0, canvas.width, canvas.height)
    if ($('.l000_torp000_element').length > 0) {
      // console.log('links', configObj.torpData.links)
      configObj.torpData.links.forEach((v, i) => {
        context.lineWidth = 2
        const startX = $('.' + v.source).offset().left - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true) - 6) + $('.l000_opera000_view').scrollLeft()
        const startY = $('.' + v.source).offset().top - ($('.l000_opera000_view').offset().top - 6) + $('.l000_opera000_view').scrollTop()
        let endX
        let endY
        let x
        let y
        if (e) {
          x = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view').scrollLeft()
          y = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top) + $('.l000_opera000_view').scrollTop()
        } else {
          x = 0
          y = 0
        }
        if (v.target) {
          // console.log('555000', v.target)
          // console.log('666000', $('.' + v.target))
          // console.log('777000', $('#' + configObj.mainBoxId).offset().left)
          // console.log('888000', $('.l000_left000_view').outerWidth(true))

          // console.log('vvv!!!!!', v)
          // console.log('v.target!!!!!', v.target)
          // console.log('left!!!!!', $('.' + v.target))
          // console.log('configObj.mainBoxId!!!!!', $('.' + configObj.mainBoxId))
          // console.log('11222223', $('#' + configObj.mainBoxId).offset().left)
          // console.log('11222224', $('.l000_left000_view').outerWidth(true))
          // console.log('11222225', $('.l000_opera000_view').scrollLeft())
          endX = $('.' + v.target).offset().left - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true) - 6) + $('.l000_opera000_view').scrollLeft()
          endY = $('.' + v.target).offset().top - ($('.l000_opera000_view').offset().top - 6) + $('.l000_opera000_view').scrollTop()
        } else {
          endX = (e ? e.originalEvent.pageX : 0) - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view').scrollLeft()
          endY = (e ? e.originalEvent.pageY : 0) - ($('.l000_opera000_view').offset().top) + $('.l000_opera000_view').scrollTop()
        }
        drawArrow(canvas, context, { x: startX, y: startY }, { x: endX, y: endY }, x, y, ischeckClick, v.arrowType, v)
      })
    }
    if (configObj.torpData.lines.length > 0) {
      configObj.torpData.lines.forEach((v, i) => {
        context.lineWidth = 8
        const startX = v.start.x
        const startY = v.start.y
        let endX
        let endY
        let x
        let y
        if (e) {
          x = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view').scrollLeft()
          y = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top) + $('.l000_opera000_view').scrollTop()
        } else {
          x = 0
          y = 0
        }
        if (v.end) {
          endX = v.end.x
          endY = v.end.y
        } else {
          endX = (e ? e.originalEvent.pageX : 0) - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view').scrollLeft()
          endY = (e ? e.originalEvent.pageY : 0) - ($('.l000_opera000_view').offset().top) + $('.l000_opera000_view').scrollTop()
          if (Math.abs(endX - startX) > Math.abs(endY - startY)) {
            endY = startY
          } else {
            endX = startX
          }
        }
        drawArrow(canvas, context, { x: startX, y: startY }, { x: endX, y: endY }, x, y, ischeckClick, 'none', v)
      })
    }
  }
  // 长按操作判断
  const longPress = () => {
    configObj.timeOutEvent = 0
    // if(confirm('是否删除该元素？')){}
  }
  // 添加锚点方法
  const addPoint = (element) => {
    const point = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'top').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
    const point2 = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'right').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
    const point3 = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'bottom').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
    const point4 = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'left').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
  }
  // 判断是否有重复连线方法
  const hasLine = (targetId) => {
    let result = false
    const sourceId = configObj.torpData.links[configObj.torpData.links.length - 1]['source'].split('000_')[2]
    configObj.torpData.links.forEach((v, i) => {
      if (i < configObj.torpData.links.length - 1) {
        if ((v.source.indexOf(targetId) > -1 && v.target.indexOf(sourceId) > -1) || (v.source.indexOf(sourceId) > -1 && v.target.indexOf(targetId) > -1)) {
          result = true
        }
      }
    })
    return result
  }
  // 绘制箭头样式方法
  const drawArrow = (canvas, context, start, end, mouseX, mouseY, ischeckClick, arrowType, dataObj) => {
    // 计算两点距离，主要是为了计算斜率
    let distanceX = end.x - start.x, distanceY = end.y - start.y
    const distance = Math.sqrt(distanceY * distanceY + distanceX * distanceX)
    // 箭头的尺寸
    let distanceArrowType = 15, sharpeArrowType = 7
    // 先确定轴线与三角两个尖角点交汇坐标
    const arrowTypeMoveTo = {
      x: start.x + distanceArrowType * distanceX / distance,
      y: start.y + distanceArrowType * distanceY / distance
    }
    const arrowTypeLineTo = {
      x: end.x - distanceArrowType * distanceX / distance,
      y: end.y - distanceArrowType * distanceY / distance
    }
    // 4个对称点坐标
    const arrowTypeTo1 = {
      x: arrowTypeMoveTo.x - sharpeArrowType * distanceY / distance,
      y: arrowTypeMoveTo.y + sharpeArrowType * distanceX / distance
    }
    const arrowTypeTo2 = {
      x: arrowTypeMoveTo.x + sharpeArrowType * distanceY / distance,
      y: arrowTypeMoveTo.y - sharpeArrowType * distanceX / distance
    }
    const arrowTypeTo3 = {
      x: arrowTypeLineTo.x - sharpeArrowType * distanceY / distance,
      y: arrowTypeLineTo.y + sharpeArrowType * distanceX / distance
    }
    const arrowTypeTo4 = {
      x: arrowTypeLineTo.x + sharpeArrowType * distanceY / distance,
      y: arrowTypeLineTo.y - sharpeArrowType * distanceX / distance
    }
    arrowType = arrowType || 'single'
    if (dataObj.isDash) {
      context.setLineDash([5, 10])
    } else {
      context.setLineDash([])
    }
    // 开始绘制
    context.beginPath()
    // 三种箭头类型
    switch (arrowType) {
      case 'single': {
        context.moveTo(start.x, start.y)
        context.lineTo(end.x, end.y)
        // 两个结束对称点
        context.lineTo(arrowTypeTo3.x, arrowTypeTo3.y)
        context.lineTo(arrowTypeTo4.x, arrowTypeTo4.y)
        // 回到结束点
        context.lineTo(end.x, end.y)
        break
      }
      case 'both': {
        context.moveTo(start.x, start.y)
        // 两个起始对称点
        context.lineTo(arrowTypeTo1.x, arrowTypeTo1.y)
        context.lineTo(arrowTypeTo2.x, arrowTypeTo2.y)
        // 回到起始点
        context.lineTo(start.x, start.y)
        // 重复single的绘制
        context.lineTo(end.x, end.y)
        context.lineTo(arrowTypeTo3.x, arrowTypeTo3.y)
        context.lineTo(arrowTypeTo4.x, arrowTypeTo4.y)
        context.lineTo(end.x, end.y)
        break
      }
      case 'none': {
        context.moveTo(start.x, start.y)
        context.lineTo(end.x, end.y)
        break
      }
    }

    // 闭合，描边与填充
    context.closePath()
    // console.log('context123', JSON.stringify(context))
    if (context.isPointInPath(mouseX, mouseY) || context.isPointInStroke(mouseX, mouseY)) {
    //   console.log('dataObj123', JSON.stringify(dataObj))
      if (dataObj.id.split('000_')[1] === 'lines') {
        // if($('.l000_left000_active').attr('data-type') === 'linear'){
        //     if(ischeckClick && confirm('确认删除此线段吗？')){
        //         let rsaultArr = [];
        //         configObj.torpData.lines.forEach((v)=>{
        //             if(v.id !== dataObj.id){
        //                 rsaultArr.push(v);
        //             }
        //         });
        //         configObj.torpData.lines = rsaultArr;
        //     }
        // }
      } else if (dataObj.id.split('000_')[1] === 'line') {
        $('.connection_status').text('')
        $('.link_bandwidth').text('')
        $('.link_used').text('')
        $('.source_if_ip').text('')
        $('.source_if_port_channel').text('')
        $('.select_value').empty()
        var after_value_array = []
        var before_value_array = []
        if (ischeckClick) {
          init_element_form('lines', dataObj)
          if (configObj.onlyDrag) {
            $('.l000_win h5').text('链接信息')
            const source_both = dataObj.source.split('000_')[2]
            const target_both = dataObj.target.split('000_')[2]
            for (const iterator of dataObj.diy_attr.all_data.topology[0]['link']) {
              if ((iterator.source['source-node'] === source_both && iterator.destination['dest-node'] === target_both)) {
                // $('.select_value').empty()
                // console.log('??????????111111', iterator.source['source-tp'], iterator.destination['dest-tp'])
                $('.select_value').append("<option value='" + iterator.source['source-tp'] + "'>" + iterator.source['source-tp'] + '</option>')
                after_value_array.push(iterator.destination['dest-tp'])
                before_value_array.push(iterator.source['source-tp'])
              } else if ((iterator.source['source-node'] === target_both && iterator.destination['dest-node'] === source_both)) {
                // console.log('??????????222222', iterator.source['source-tp'], iterator.destination['dest-tp'])
                $('.select_value').append("<option value='" + iterator.source['source-tp'] + "'>" + iterator.source['source-tp'] + '</option>')
                after_value_array.push(iterator.destination['dest-tp'])
                before_value_array.push(iterator.source['source-tp'])
              }

              $('.after_value').text(after_value_array[0])
              // console.log('7777778', $('.select_value').val())
            }
            dataObj.diy_attr.all_data.topology[0]['link'].forEach(element => {
              if (element.source['source-tp'] === before_value_array[0] && element.destination['dest-tp'] === after_value_array[0]) {
                // console.log('qqq123', element['bandwidth'])
                // console.log('333', element['bandwidth-used'])
                // console.log('333444', element['status'])
                if (element.hasOwnProperty('bandwidth')) {
                  $('.link_bandwidth').text(element['bandwidth'])
                } else {
                  $('.link_bandwidth').text('')
                }
                if (element.hasOwnProperty('bandwidth-used')) {
                  $('.link_used').text(element['bandwidth-used'])
                } else {
                  $('.link_used').text('')
                }
                if (element['status'] === 'Connected') {
                  $('.connection_status').text('正常')
                } else {
                  $('.connection_status').text('异常')
                }
                if (element.hasOwnProperty('source-if-ip')) {
                  $('.source_if_ip').text(element['source-if-ip'])
                } else {
                  $('.source_if_ip').text('')
                }
                if (element.hasOwnProperty('source-if-port-channel')) {
                  $('.source_if_port_channel').text(element['source-if-port-channel'])
                } else {
                  $('.source_if_port_channel').text('')
                }
              }
            })
            // console.log('66668888', before_value_array)
            // console.log('77778888', before_value_array.length)
            // console.log('66668888', after_value_array)
            // console.log('77778888', after_value_array.length)
            // 图标双向单向
            // if (dataObj.arrowType === 'single') {
            //   $('.select_value').append("<option value='" + dataObj.diy_attr['link-id'] + "'>" + dataObj.diy_attr['link-id'] + '</option>')
            // } else if (dataObj.arrowType === 'both') {
            //   const source_both = dataObj.source.split('000_')[2]
            //   const target_both = dataObj.target.split('000_')[2]
            //   console.log('1', source_both)
            //   console.log('2', target_both)
            //   for (const iterator of dataObj.diy_attr.all_data.topology[0]['link']) {
            //     console.log('3', iterator.source['source-node'])
            //     console.log('4', iterator.destination['dest-node'])
            //     if ((iterator.source['source-node'] === source_both && iterator.destination['dest-node'] === target_both)) {
            //       console.log('??????????111111', iterator.source['source-tp'], iterator.destination['dest-tp'])
            //       $('.select_value').append("<option value='" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + "'>" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + '</option>')
            //     } else if ((iterator.source['source-node'] === target_both && iterator.destination['dest-node'] === source_both)) {
            //       console.log('??????????222222', iterator.source['source-tp'], iterator.destination['dest-tp'])
            //       $('.select_value').append("<option value='" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + "'>" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + '</option>')
            //     }
            //   }
            // }
            // console.log('777777', $('.select_value').val())
            var arg_init = ''
            arg_init = $('.select_value').val().split('::')[0]
            const source_tp_init = $('.select_value').val().split('::')[1]
            var host_arg_init = ''
            for (const iteratorArg of dataObj.diy_attr.all_data.topology[0]['node']) {
              // console.log('00011', iteratorArg['node-id'])
              // console.log('00012', arg_init)
              var arg_init_2 = arg_init
              const reg = new RegExp('\\.', 'g')
              arg_init_2 = arg_init_2.replace(reg, '-')
              const reg2 = new RegExp(':', 'g')
              arg_init_2 = arg_init_2.replace(reg2, '-')
              if (iteratorArg['node-id'] === arg_init_2) {
                host_arg_init = iteratorArg['host']
              }
            }
            var bol_value = false
            var source_tp = ''
            var host_arg = ''
            var arg = ''
            $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg_init + '&var-Device=' + host_arg_init + '&var-Interface=' + source_tp_init + '&refresh=30s&kiosk')
            $('.select_value').change(function() {
              bol_value = true
              const str = ''
              // $('.select_value option:selected').each(function() {
              //   str = $(this).text()
              // })
              // console.log('str444', str)
              // console.log('before_value_array444', before_value_array)
              const before_index = $('option:selected', '.select_value').index()
              // console.log('before_index666', before_index)
              $('.after_value').text(after_value_array[before_index])
              arg = $(this).val().split('::')[0]
              source_tp = $(this).val().split('::')[1]
              for (const iteratorArg of dataObj.diy_attr.all_data.topology[0]['node']) {
                const reg = new RegExp('\\.', 'g')
                arg = arg.replace(reg, '-')
                const reg2 = new RegExp(':', 'g')
                arg = arg.replace(reg2, '-')
                // console.log('oooo', iteratorArg['node-id'])
                // console.log('ooooarg123', arg)
                if (iteratorArg['node-id'] === arg) {
                  host_arg = iteratorArg['host']
                }
              }
              // console.log('00000', $(this).val())
              // console.log('11111', after_value_array[before_index])
              dataObj.diy_attr.all_data.topology[0]['link'].forEach(element => {
                if (element.source['source-tp'] === $(this).val() && element.destination['dest-tp'] === after_value_array[before_index]) {
                  // console.log('222', element['bandwidth'])
                  // console.log('333', element['bandwidth-used'])
                  if (element.hasOwnProperty('bandwidth')) {
                    $('.link_bandwidth').text(element['bandwidth'])
                  } else {
                    $('.link_bandwidth').text('')
                  }
                  if (element.hasOwnProperty('bandwidth-used')) {
                    $('.link_used').text(element['bandwidth-used'])
                  } else {
                    $('.link_used').text('')
                  }
                  if (element['status'] === 'Connected') {
                    $('.connection_status').text('正常')
                  } else {
                    $('.connection_status').text('异常')
                  }
                  if (element.hasOwnProperty('source-if-ip')) {
                    $('.source_if_ip').text(element['source-if-ip'])
                  } else {
                    $('.source_if_ip').text('')
                  }
                  if (element.hasOwnProperty('source-if-port-channel')) {
                    $('.source_if_port_channel').text(element['source-if-port-channel'])
                  } else {
                    $('.source_if_port_channel').text('')
                  }
                }
              })
              // console.log('host_arg123', host_arg)
              // console.log('source_tp123', source_tp)
              // console.log('host_arg123444444', dataObj.diy_attr['bandwidth'])
              // console.log('source_tp12344444', dataObj.diy_attr)

              $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg + '&var-Device=' + host_arg + '&var-Interface=' + source_tp + '&refresh=30s&kiosk')
            })
            $('.btn_reset').click(function() {
              // console.log('bol_value123', bol_value)
              // console.log('host_arg_init', host_arg_init)
              // console.log('source_tp_init', source_tp_init)
              // console.log('host_arg', host_arg)
              // console.log('source_tp', source_tp)
              $('.monitoring_iframe').prop('src', '')
              if (bol_value === false) {
                $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg_init + '&var-Device=' + host_arg_init + '&var-Interface=' + source_tp_init + '&refresh=30s&kiosk')
              } else if (bol_value === true) {
                $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg + '&var-Device=' + host_arg + '&var-Interface=' + source_tp + '&refresh=30s&kiosk')
              }
            })
            // $('#l000_link000_info').show()
            // $('#l000_mach000_info').hide()
            $('.l000_win').show()
            $('.l000_win_device').hide()
            $('.l000_mask').fadeIn()
          }
        }
        $('.l000_torp000_info000_window').attr('data-id', dataObj.id).empty()
        $('<p>元素ID：' + dataObj.id + '</p>').appendTo('.l000_torp000_info000_window')
        $('<p>元素名称：' + dataObj.name + '</p>').appendTo('.l000_torp000_info000_window')
        if (Object.keys(dataObj.diy_attr).length > 0) {
          $('<p>自定义属性：{</p>').appendTo('.l000_torp000_info000_window')
          Object.keys(dataObj.diy_attr).forEach((v) => {
            $('<p style="text-indent: 20px;">' + v + ':' + dataObj.diy_attr[v] + ',</p>').appendTo('.l000_torp000_info000_window')
          })
          $('<p>}</p>').appendTo('.l000_torp000_info000_window')
        }

        configObj.hoverFlag = true
      }
      context.fillStyle = '#3d7fbb'
      context.strokeStyle = '#44dcd7'
	  context.lineWidth=4
    } else {
      context.fillStyle = dataObj.color
      context.strokeStyle = dataObj.color
    }
    context.stroke()
    context.fill()
  }
  // 根据元素点击事件，渲染右侧属性表单
  const init_element_form = (type, dataObj) => {
    const _self = this
    if (type === 'lines') {
      let colorFlag = false
      $('.l000_line000_box').find('li.l000_diy000_li').remove()
      $('.l000_line000_id').val(dataObj.id).attr('data-old-id', dataObj.id)
      $('.l000_line000_name').val(dataObj.name)
      $('.l000_line000_style').val(dataObj.isDash ? 'dash' : 'line')
      $('.l000_arrow000_style').val(dataObj.arrowType)
      $('.l000_line000_color option').each(function() {
        if ($(this).val() === dataObj.color) {
          colorFlag = true
        }
      })
      if (colorFlag) {
        $('.l000_line000_color').val(dataObj.color)
        $('.l000_diy000_color').hide()
      } else {
        $('.l000_line000_color').val('-1')
        $('#l000_color000_input').val(dataObj.color.replace('#', ''))
        $('#l000_color').css('background', dataObj.color)
        $('.l000_diy000_color').show()
      }
      $('.l000_line000_box').attr('data-line-id', dataObj.id).show()
      $('.l000_element000_box').hide()

      configObj.torpData.links.forEach((v) => {
        if (v.id === dataObj.id) {
          $('.l000_line000_box').find('.l000_nomargin').find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          $('.l000_line000_box').find('li.l000_diy000_input000_box').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('input').val('')
            }
          })
          $('.l000_line000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          configObj.torpData.links.forEach((v) => {
            if (v.id === dataObj.id) {
              if (Object.keys(v.diy_attr).length > 0) {
                Object.keys(v.diy_attr).forEach((j) => {
                  const diy_ipt = $('<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名" value="' + j + '">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值" value="' + v.diy_attr[j] + '"><span class="l000_delete000_diy000_style">+</span></li>')
                  const diyAttr = $('<p>“<span class="l000_key">' + j + '</span>”:”<span class="l000_value">' + v.diy_attr[j] + '</span>”,</p>')
                  const diyHtmlAttr = $('<p>data-torp-<span class="l000_data000_attr000_key">' + j + '</span>=“<span class="l000_data000_attr000_value">' + v.diy_attr[j] + '</span>”</p>')
                  $('.l000_line000_box').find('.l000_add000_diy000_style').before(diy_ipt)
                  $('.l000_line000_box').find('.l000_nomargin').append(diyAttr)
                  $('.l000_line000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).append(diyHtmlAttr)
                  diy_ipt.find('input').on('input', function() {
                    const liIdx = $(this).parent().index() - 3
                    const iptIdx = $(this).index()
                    const val = $(this).val()
                    $(this).parents('ul.l000_form000_ul').find('li').each(function() {
                      $(this).find('p').each(function(i) {
                        if (i === liIdx) {
                          $(this).find('span').eq(iptIdx).text(val)
                        }
                      })
                    })
                  }).on('blur', function(e) {
                    e.preventDefault()
                    if ($(this).parent().find('input').eq(0).val() == '') {
                      $(this).parent().find('input').eq(0).val('diy_attr_' + new Date().getTime())
                    } else {
                      const idx = $(this).parent().index() - 3
                      const val = $(this).parent().find('input').eq(0).val()
                      let flag = true
                      diy_ipt.parent().find('li.l000_diy000_input000_box').each(function(i) {
                        if (i !== idx && $(this).find('input').eq(0).val() === val) {
                          flag = false
                        }
                      })
                      if (flag) {
                        updateDiyAttr('data-line-id', 'links', diy_ipt.parent())
                      } else {
                        alert('自定义属性名不可以重复！')
                        $(this).parent().find('input').eq(0).val('')
                        const val2 = $(this).parent().find('input').eq(1).val()
                        const idx = $(this).parent().index() - 3
                        $(this).parent().siblings('ul').find('li').each(function() {
                          $(this).find('p').each(function(i) {
                            if (i === idx) {
                              $(this).find('span').eq(0).text('')
                              $(this).find('span').eq(1).text(val2)
                            }
                          })
                        })
                      }
                    }
                  })
                  diy_ipt.find('.l000_delete000_diy000_style').on('click', function(e) {
                    e.stopPropagation()
                    e.preventDefault()
                    if (diy_ipt.parent().find('.l000_delete000_diy000_style').length < 2) {
                      $(this).parent().find('input').eq(0).val('')
                      $(this).parent().find('input').eq(1).val('')
                      const idx = $(this).parent().index() - 3
                      $(this).parent().siblings('ul').find('li').each(function() {
                        $(this).find('p').each(function(i) {
                          if (i === idx) {
                            $(this).find('span').eq(0).text('')
                            $(this).find('span').eq(1).text('')
                          }
                        })
                      })
                    } else {
                      const idx = $(this).parent().index() - 3
                      $(this).parent().siblings('ul').find('li').each(function() {
                        $(this).find('p').each(function(i) {
                          if (i === idx) {
                            $(this).remove()
                          }
                        })
                      })
                      $(this).parent().remove()
                    }
                    updateDiyAttr('data-line-id', 'links', diy_ipt.parent())
                  })
                })
              }
            }
          })
        }
      })
    }
    if (type === 'nodes') {
      $('.l000_line000_box').attr('data-line-id', '').hide()
      $('.l000_element000_name').val(dataObj.attr('data-name'))
      $('.l000_element000_id').attr('data-old-id', dataObj.prop('id')).val(dataObj.prop('id'))
      $('.l000_element000_box').find('li.l000_diy000_li').remove()
      $('.l000_element000_box').attr('data-element-id', dataObj.prop('id')).show()
      $('.l000_element000_style').val(dataObj.attr('data-background-id')).change()

      configObj.torpData.nodes.forEach((v) => {
        if (v.id === dataObj.prop('id')) {
          $('.l000_element000_box').find('.l000_nomargin').find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          $('.l000_element000_box').find('li.l000_dify000_input000_box').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('input').val('')
            }
          })
          $('.l000_element000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          if (Object.keys(v.diy_attr).length > 0) {
            Object.keys(v.diy_attr).forEach((j) => {
              const diy_ipt = $('<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名" value="' + j + '">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值" value="' + v.diy_attr[j] + '"><span class="l000_delete000_diy000_style">+</span></li>')
              const diyAttr = $('<p>“<span class="l000_key">' + j + '</span>”:”<span class="l000_value">' + v.diy_attr[j] + '</span>”,</p>')
              const diyHtmlAttr = $('<p>data-torp-<span class="l000_data000_attr000_key">' + j + '</span>=“<span class="l000_data000_attr000_value">' + v.diy_attr[j] + '</span>”</p>')
              $('.l000_element000_box').find('.l000_add000_diy000_style').before(diy_ipt)
              $('.l000_element000_box').find('.l000_nomargin').append(diyAttr)
              $('.l000_element000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).append(diyHtmlAttr)
              diy_ipt.find('input').on('input', function() {
                const liIdx = $(this).parent().index() - 3
                const iptIdx = $(this).index()
                const val = $(this).val()
                $(this).parents('ul.l000_form000_ul').find('li').each(function() {
                  $(this).find('p').each(function(i) {
                    if (i === liIdx) {
                      $(this).find('span').eq(iptIdx).text(val)
                    }
                  })
                })
              }).on('blur', function(e) {
                e.preventDefault()
                if ($(this).parent().find('input').eq(0).val() == '') {
                  $(this).parent().find('input').eq(0).val('diy_attr_' + new Date().getTime())
                } else {
                  const idx = $(this).parent().index() - 3
                  const val = $(this).parent().find('input').eq(0).val()
                  let flag = true
                  diy_ipt.parent().find('li.l000_diy000_input000_box').each(function(i) {
                    if (i !== idx && $(this).find('input').eq(0).val() === val) {
                      flag = false
                    }
                  })
                  if (flag) {
                    updateDiyAttr('data-element-id', 'nodes', diy_ipt.parent())
                  } else {
                    alert('自定义属性名不可以重复！')
                    $(this).parent().find('input').eq(0).val('')
                    const val2 = $(this).parent().find('input').eq(1).val()
                    const idx = $(this).parent().index() - 3
                    $(this).parent().siblings('ul').find('li').each(function() {
                      $(this).find('p').each(function(i) {
                        if (i === idx) {
                          $(this).find('span').eq(0).text('')
                          $(this).find('span').eq(1).text(val2)
                        }
                      })
                    })
                  }
                }
              })
              diy_ipt.find('.l000_delete000_diy000_style').on('click', function(e) {
                e.stopPropagation()
                e.preventDefault()
                if (diy_ipt.parent().find('.l000_delete000_diy000_style').length < 2) {
                  $(this).parent().find('input').eq(0).val('')
                  $(this).parent().find('input').eq(1).val('')
                  const idx = $(this).parent().index() - 3
                  $(this).parent().siblings('ul').find('li').each(function() {
                    $(this).find('p').each(function(i) {
                      if (i === idx) {
                        $(this).find('span').eq(0).text('')
                        $(this).find('span').eq(1).text('')
                      }
                    })
                  })
                } else {
                  const idx = $(this).parent().index() - 3
                  $(this).parent().siblings('ul').find('li').each(function() {
                    $(this).find('p').each(function(i) {
                      if (i === idx) {
                        $(this).remove()
                      }
                    })
                  })
                  $(this).parent().remove()
                }
                updateDiyAttr('data-element-id', 'nodes', diy_ipt.parent())
              })
            })
          }
        }
      })
    }
  }
  // 导出json文件方法
  const saveJSON = (data, sendAxios, filename) => {
    if (!data) {
      alert('保存的数据为空')
      return
    }
    if (sendAxios) {
      alert('此处发送请求保存数据的接口')
    } else {
      if (!filename) { filename = 'json.json' }
      if (typeof data === 'object') {
        data = JSON.stringify(data, undefined, 4)
      }
      let blob = new Blob([data], { type: 'text/json' }),
        e = document.createEvent('MouseEvents'),
        a = document.createElement('a')
      a.download = filename
      a.href = window.URL.createObjectURL(blob)
      a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
      e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
      a.dispatchEvent(e)
    }
  }
  // 读取文件方法
  const handleFiles = function(selectedFile) {
    if (selectedFile) {
      const _self = this
      var reader = new FileReader()
      reader.readAsText(selectedFile)// 读取文件的内容
      reader.onload = function() {
        const json = JSON.parse(this.result)
        if (Object.prototype.toString.call(json.nodes) === '[object Array]' && Object.prototype.toString.call(json.links) === '[object Array]' && Object.prototype.toString.call(json.lines) === '[object Array]' && Object.prototype.toString.call(json.text) === '[object Array]') {
          configObj.torpData = json
          $('#' + configObj.mainBoxId).empty()
          _self.init.call(_self)
          json.nodes.forEach((v) => {
            const elBox = $('<div>').addClass('l000_torp000_element').css({ 'top': v.y + 'px', 'left': v.x + 'px' }).appendTo($('.l000_opera000_view'))
            const closeBtn = $('<div>+</div>').addClass('l000_del000_torp').appendTo(elBox)
            const div = $('<div><p>' + v.name + '</p></div>').attr({ 'id': v.id, 'data-name': v.name, 'data-background-id': v.background_id }).addClass('l000_drag000_element').css({ 'background': v.background + ' #fff center no-repeat', 'background-size': '100% 100%' }).appendTo(elBox)
            // 添加连线锚点方法
            addPoint(elBox)
            // 改变clone元素的绑定事件方法
            changeBind(div)
            closeBtn.on('click', (e) => {
              if (confirm('确认删除此元素吗？')) {
                $('.l000_right000_box').hide()
                $('#l000_img000_file').val('')
                $('#img_view').css('background', '#ccc')

                elBox.remove()
                const afterDeleteNodeArr = []
                configObj.torpData.nodes.forEach((v) => {
                  if (v.id !== div.prop('id')) {
                    afterDeleteNodeArr.push(v)
                  }
                })
                configObj.torpData.nodes = afterDeleteNodeArr
                const afterDeletePositionArr = []
                configObj.torpData.links.forEach((v) => {
                  if (v.source.indexOf(div.prop('id').split('000_')[2]) < 0 && v.target.indexOf(div.prop('id').split('000_')[2]) < 0) {
                    afterDeletePositionArr.push(v)
                  }
                })
                configObj.torpData.links = afterDeletePositionArr
                refreshCanvas($('#' + configObj.canvasId), e, false)
              }
            })
          })
          json.links.forEach((v) => {
            addDotClass(v.source)
            addDotClass(v.target)
          })
          refreshCanvas($('#' + configObj.canvasId), undefined, false)
        } else {
          alert('导入文件的数据格式不正确！')
        }
      }
    }
  }
  // 添加锚点class
  const addDotClass = (val) => {
    $('#l000_torp000_' + val.split('000_')[2]).parent().find('.l000_torp000_dot').each(function() {
      if ($(this).attr('data-position') === val.split('000_')[1]) {
        $(this).addClass(val)
      }
    })
  }
  // 更新自定义属性
  const updateDiyAttr = (attr, key, template) => {
    configObj.torpData[key].forEach((v) => {
      if (v.id === template.parent().attr(attr)) {
        v.diy_attr = {}
        template.find('li.l000_diy000_input000_box').each(function() {
          v.diy_attr[$(this).find('input').eq(0).val()] = $(this).find('input').eq(1).val()
        })
      }
    })
  }
  // 计算位置重叠方法
  const computPosition = (posotion, num, el) => {
    let count = 0;
    (el ? el.siblings('.l000_torp000_element') : $('.l000_torp000_element')).each(function() {
      const inX = parseFloat($(this).css('left').replace('px', '')) < (posotion.left + num) && parseFloat($(this).css('left').replace('px', '')) > (posotion.left - num)
      const inY = parseFloat($(this).css('top').replace('px', '')) < (posotion.top + num) && parseFloat($(this).css('top').replace('px', '')) > (posotion.top - num)
      if (inX && inY) {
        count++
      }
    })
    if (count > 0) {
      return computPosition({ top: posotion.top + 50, left: posotion.left + 50 }, num); f
    } else {
      return posotion
    }
  }
  // 计算浮窗位置及避免边界碰撞方法
  const computInfoWindowPosition = (e) => {
    const windowX = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true))
    const windowY = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top)
      // const windowX = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)+120)
      // const windowY = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top+100)
      // console.log('windowX',windowX);
      // console.log('windowY',windowY);
    const limitX = $('.l000_opera000_view').outerWidth(true) - $('.l000_torp000_info000_window').outerWidth(true)
    const limitY = $('.l000_opera000_view').outerHeight(true) - $('.l000_torp000_info000_window').outerHeight(true)
    const position = {
      top: windowY,
      left: windowX,
      right: 'unset',
      bottom: 'unset'
    }
    if (windowX >= limitX) {
      position.left = 'unset'
      position.right = $('.l000_opera000_view').outerWidth(true) - windowX + 20
    }
    if (windowY >= limitY) {
      position.top = 'unset'
      position.bottom = $('.l000_opera000_view').outerHeight(true) - windowY + 20
    }
    return JSON.stringify(position)
  }
  // 获取拓扑数据
  this.getTorpData = () => {
    return configObj.torpData
  }
  // 设置拓扑数据
  this.setTorpData = (data) => {
    // console.log('data666', data)
    // console.log('data777', init_data)
    var all_data = data
    const isArry = Object.prototype.toString.call(data) === '[object Object]';
    const hasNode = Object.prototype.toString.call(data.nodes) === '[object Array]';
    const hasLinkes = Object.prototype.toString.call(data.links) === '[object Array]';
    if (isArry && hasNode && hasLinkes) {
      configObj.torpData = data
      $('#' + configObj.mainBoxId).empty()
      this.init()
      var init_arr = []
      // init_data.topology[0].node.forEach((j, h) => {
      //   const reg5 = new RegExp('\\.', 'g')
      //   if (j['node-id'].match(reg5)) {
      //     console.log('h123', h)
      //     init_arr.push(h)
      //   }
      // })
      data.nodes.forEach((v, w) => {        
        const elBox = $('<div>').addClass('l000_torp000_element ' + v.otherClassName).css({ 'top': v.y + 'px', 'left': v.x + 'px' }).appendTo($('.l000_opera000_view'))
        elBox.attr('data-win', JSON.stringify({
          'machId': v.oraData['node-id'],
          'machType': v.oraData['device-family'],
          'machTypeName': v.oraData['device-type'],
          'host': v.oraData['host'],
          'buttonInfo': v.oraData['urls']
        }))
        // console.log('w123', w)
        // array.forEach(element => {

        // })
        const div = $('<div><p>' + v.name + '</p></div>').attr({ 'id': v.id, 'data-name': v.name, 'data-background-id': v.background_id }).addClass('l000_drag000_element').css({ 'background': v.background + ' #fff center no-repeat', 'background-size': '100% 100%' }).appendTo(elBox)
        // 添加连线锚点方法
        addPoint(elBox)

        if (configObj.onlyDrag) {
          changeBind(div)
        }
        if (configObj.couldEdit) {
          const closeBtn = $('<div>+</div>').addClass('l000_del000_torp').appendTo(elBox)
          // 改变clone元素的绑定事件方法
          changeBind(div)
          closeBtn.on('click', (e) => {
            if (confirm('确认删除此元素吗？')) {
              $('.l000_right000_box').hide()
              $('#l000_img000_file').val('')
              $('#img_view').css('background', '#ccc')

              elBox.remove()
              const afterDeleteNodeArr = []
              configObj.torpData.nodes.forEach((v) => {
                if (v.id !== div.prop('id')) {
                  afterDeleteNodeArr.push(v)
                }
              })
              configObj.torpData.nodes = afterDeleteNodeArr
              const afterDeletePositionArr = []
              configObj.torpData.links.forEach((v) => {
                if (v.source.indexOf(div.prop('id').split('000_')[2]) < 0 && v.target.indexOf(div.prop('id').split('000_')[2]) < 0) {
                  afterDeletePositionArr.push(v)
                }
              })
              // console.log('afterDeletePositionArr888', afterDeletePositionArr)
              configObj.torpData.links = afterDeletePositionArr
              refreshCanvas($('#' + configObj.canvasId), e, false)
            }
          })
        }
      })
      data.links.forEach((v) => {
        addDotClass(v.source)
        addDotClass(v.target)
      })
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    } else {
      alert('数据格式有误')
    }
  }

  const constructor = (conf) => {
    if (Object.prototype.toString.call(conf) === '[object Object]') {
      // 如果实例有传参，且参数是object，则执行合并配置项变量的方法
      // console.log(111111111111111111111)
      mergeObjectKey(conf, baseConfig)
    } else {
      // 如果没有参数或者参数格式不正确，则使用基本配置项
      // console.log(22222222222222222)
      mergeObjectKey(configObj, baseConfig)
    }
    this.init()
  }
  constructor(para)
}
function TopologyMap2(para) {
  const baseConfig = {
    couldEdit: true,
    onlyDrag: false,
    leftViewShow: true,
    centerViewShow: true,
    rightViewShow: true,
    leftViewWidth: 4,
    centerViewWidth: 12,
    rightViewWidth: 8,
    mainBoxId: 'torp',
    canvasId: 'l000_torp000_canvas',
    elementType: [
      {
        name: '测试图形1',
        background_id: '001',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20height%3D%221000%22%20viewBox%3D%220%200%20750%20750.00178%22%20width%3D%221000%22%3E%3Cpath%20d%3D%22M549.934%20325.008h25v25h-25zm0%200M499.934%20325.008h25v25h-25zm0%200M449.934%20325.008h25v25h-25zm0%200M174.938%20325.008h25v25h-25zm0%200M549.934%20475.008h25v25h-25zm0%200M499.934%20475.008h25v25h-25zm0%200M449.934%20475.008h25v25h-25zm0%200M174.938%20475.008h25v25h-25zm0%200%22%2F%3E%3Cpath%20d%3D%22M137.438%20575.004c-6.903%200-12.497%205.598-12.497%2012.5v100c0%206.898%205.594%2012.5%2012.496%2012.5h37.5v37.5c0%206.898%205.598%2012.496%2012.5%2012.496h50c6.903%200%2012.5-5.598%2012.5-12.496v-37.5h249.997v37.5c0%206.898%205.593%2012.496%2012.5%2012.496h50c6.902%200%2012.5-5.598%2012.5-12.496v-37.5h37.496c6.906%200%2012.5-5.602%2012.5-12.5v-100c0-6.902-5.594-12.5-12.5-12.5h-37.496v-25h37.496c6.906%200%2012.5-5.598%2012.5-12.5v-99.996c0-6.906-5.594-12.5-12.5-12.5h-37.496v-25h37.496c6.906%200%2012.5-5.602%2012.5-12.5v-100c0-6.903-5.594-12.5-12.5-12.5H137.438c-6.903%200-12.497%205.597-12.497%2012.5v100c0%206.898%205.594%2012.5%2012.496%2012.5h37.5v25h-37.5c-6.902%200-12.496%205.594-12.496%2012.5v99.996c0%206.902%205.594%2012.5%2012.496%2012.5h37.5v25zm87.5%20150h-25v-25h25zm324.996%200h-25v-25h25zm49.996-50H149.938v-75H599.93zm-99.996-125v25H249.937v-25zm50%2025h-25v-25h25zm0-149.996h-25v-25h25zm-299.996%200v-25h249.996v25zm-100-125H599.93v75H149.938zm50%20100h25v25h-25zm-50%2050H599.93v74.996H149.938zm50%2099.996h25v25h-25zm0%200%22%2F%3E%3Cpath%20d%3D%22M549.934%20625.004h25v25h-25zm0%200M499.934%20625.004h25v25h-25zm0%200M449.934%20625.004h25v25h-25zm0%200M174.938%20625.004h25v25h-25zm0%200M672.98%20214.074c1.29-8.8%201.946-17.676%201.95-26.562.03-86.524-59.168-161.828-143.254-182.215-84.082-20.39-171.2%2019.426-210.809%2096.351-25.562-25.183-60.043-39.246-95.93-39.136-75.902.09-137.406%2061.597-137.496%20137.5%200%204.222.196%208.445.586%2012.675C37.47%20215.774-1.48%20258.462.043%20309.09c1.535%2050.625%2043%2090.879%2093.648%2090.918h6.25v-25h-6.25c-37.968%200-68.75-30.781-68.75-68.75%200-37.973%2030.782-68.746%2068.75-68.746h8.75c3.754%200%207.309-1.688%209.68-4.602%202.375-2.906%203.32-6.722%202.57-10.406-1.496-7.402-2.25-14.938-2.25-22.492-.054-48.301%2030.754-91.227%2076.52-106.633%2045.773-15.41%2096.273.14%20125.437%2038.629%202.747%203.605%207.22%205.441%2011.696%204.8%204.48-.632%208.27-3.636%209.902-7.859C364.164%2055.945%20440.383%2013.402%20517.301%2027.754c76.922%2014.348%20132.68%2081.512%20132.629%20159.758-.024%2011.773-1.32%2023.5-3.875%2034.992-.801%203.652.074%207.46%202.37%2010.398%202.305%202.934%205.802%204.692%209.532%204.786%2036.598%202.253%2064.977%2032.84%2064.5%2069.503-.473%2036.664-29.633%2066.504-66.277%2067.817h-6.25v25h6.25c48.414-.133%2088.77-37.098%2093.125-85.317%204.36-48.214-28.715-91.82-76.325-100.617zm0%200%22%2F%3E%3C%2Fsvg%3E')"
      },
      {
        name: '测试图形2',
        background_id: '002',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20height%3D%221000%22%20viewBox%3D%22-162%200%20750%20750%22%20width%3D%221000%22%3E%3Cpath%20d%3D%22M412.5%200h-400C5.594%200%200%205.594%200%2012.5v700c0%206.906%205.594%2012.5%2012.5%2012.5H50v25h25v-25h275v25h25v-25h37.5c6.906%200%2012.5-5.594%2012.5-12.5v-700C425%205.594%20419.406%200%20412.5%200zM400%20700H25V25h375zm0%200%22%2F%3E%3Cpath%20d%3D%22M62.5%20675h300c6.906%200%2012.5-5.594%2012.5-12.5v-600c0-6.906-5.594-12.5-12.5-12.5h-300C55.594%2050%2050%2055.594%2050%2062.5v600c0%206.906%205.594%2012.5%2012.5%2012.5zM350%20650H75v-75h275zm0-100H75v-75h275zm0-100H75v-75h275zm0-100H75v-75h275zm0-100H75v-75h275zm0-175v75H75V75zm0%200%22%2F%3E%3Cpath%20d%3D%22M300%20100h25v25h-25zm0%200M250%20100h25v25h-25zm0%200M80%20100h125v25H100zm0%200M300%20200h25v25h-25zm0%200M250%20200h25v25h-25zm0%200M80%20200h125v25H100zm0%200M300%20300h25v25h-25zm0%200M250%20300h25v25h-25zm0%200M80%20300h125v25H100zm0%200M300%20400h25v25h-25zm0%200M250%20400h25v25h-25zm0%200M80%20400h125v25H100zm0%200M300%20500h25v25h-25zm0%200M250%20500h25v25h-25zm0%200M80%20500h125v25H100zm0%200M300%20600h25v25h-25zm0%200M250%20600h25v25h-25zm0%200M80%20600h125v25H100zm0%200%22%2F%3E%3C%2Fsvg%3E')"
      },
      {
        name: '测试图形3',
        background_id: '003',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20512%20512%22%3E%3Cpath%20d%3D%22M130%20246c-5.52%200-10%204.48-10%2010s4.48%2010%2010%2010%2010-4.48%2010-10-4.48-10-10-10z%22%2F%3E%3Cpath%20d%3D%22M256%200C118.953%200%200%20116.932%200%20256c0%20139.219%20119.11%20256%20256%20256%20137.832%200%20256-77.678%20256-256C512%20116.777%20392.886%200%20256%200zm180.145%20106.199c33.835%2040.246%2053.341%2089.305%2055.623%20139.801H452v-30c0-16.542-13.458-30-30-30h-35.089c-3.106-20.556-7.755-40.444-13.875-59.354%2023.071-5.423%2044.221-12.281%2063.109-20.447zm-14.358-15.677c-16.714%206.729-35.566%2012.553-55.512%2017.152-13.126-33.552-30.229-60.607-49.392-79.204%2038.915%2010.951%2075.167%2032.233%20104.904%2062.052zM266%2021.077c29.768%206.334%2059.944%2040.245%2080.386%2090.711-26.063%204.787-53.471%207.546-80.386%208.099v-98.81zm0%20118.813c29.271-.578%2059.119-3.675%2087.363-9.068%205.804%2017.552%2010.26%2036.039%2013.309%2055.178H266v-46.11zM246%2021.077v98.81c-26.915-.552-54.322-3.311-80.386-8.099C186.056%2061.321%20216.232%2027.41%20246%2021.077zm0%20118.813V186H145.328c3.048-19.138%207.505-37.626%2013.309-55.177%2028.244%205.392%2058.092%208.489%2087.363%209.067zM195.118%2028.469c-19.164%2018.598-36.266%2045.653-49.392%2079.205-19.946-4.599-38.798-10.422-55.513-17.152%2029.736-29.819%2065.989-51.101%20104.905-62.053zm-79.263%2077.73c18.888%208.166%2040.039%2015.024%2063.109%2020.447-6.119%2018.91-10.769%2038.798-13.875%2059.354H90c-16.542%200-30%2013.458-30%2030v30H20.232c2.282-50.496%2021.788-99.555%2055.623-139.801zm0%20299.602C42.02%20365.555%2022.514%20316.496%2020.232%20266H60v30c0%2016.542%2013.458%2030%2030%2030h35.089c3.106%2020.556%207.755%2040.444%2013.875%2059.354-23.071%205.423-44.221%2012.281-63.109%2020.447zm14.358%2015.677c16.714-6.729%2035.567-12.553%2055.512-17.152%2013.126%2033.552%2030.229%2060.607%2049.392%2079.204-38.915-10.951-75.168-32.233-104.904-62.052zM246%20490.923c-29.768-6.334-59.944-40.245-80.386-90.711%2026.063-4.787%2053.471-7.546%2080.386-8.099v98.81zM246%20326v46.11c-29.271.578-59.119%203.675-87.363%209.068-5.804-17.552-10.26-36.039-13.309-55.178H246zM90%20306c-5.514%200-10-4.486-10-10v-80c0-5.514%204.486-10%2010-10h288.186l.021.001.015-.001H422c5.514%200%2010%204.486%2010%2010v80c0%205.514-4.486%2010-10%2010H90zm276.672%2019.9c-3.048%2019.138-7.505%2037.726-13.309%2055.277-28.244-5.392-58.092-8.489-87.363-9.067V325.9h100.672zM266%20490.923v-98.81c26.915.552%2054.322%203.311%2080.386%208.099-20.442%2050.467-50.618%2084.378-80.386%2090.711zm50.882-7.392c19.164-18.598%2036.266-45.653%2049.392-79.205%2019.946%204.599%2038.798%2010.422%2055.513%2017.152-29.736%2029.819-65.989%2051.101-104.905%2062.053zm119.263-77.73c-18.888-8.166-40.039-15.024-63.109-20.447%206.119-18.91%2010.769-38.798%2013.875-59.354H422c16.542%200%2030-13.458%2030-30v-30.1h39.768c-2.282%2050.496-21.788%2099.655-55.623%20139.901z%22%2F%3E%3Cpath%20d%3D%22M210%20246h-40c-5.522%200-10%204.477-10%2010s4.478%2010%2010%2010h40c5.522%200%2010-4.477%2010-10s-4.478-10-10-10zM302%20246h-46c-5.522%200-10%204.477-10%2010s4.478%2010%2010%2010h46c5.522%200%2010-4.477%2010-10s-4.478-10-10-10zM382%20246h-40c-5.522%200-10%204.477-10%2010s4.478%2010%2010%2010h40c5.522%200%2010-4.477%2010-10s-4.478-10-10-10z%22%2F%3E%3C%2Fsvg%3E')"
      },
      {
        name: '测试图形4',
        background_id: '004',
        svg: "url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20512%20512%22%3E%3Cpath%20d%3D%22M150%2060c-5.52%200-10%204.48-10%2010s4.48%2010%2010%2010%2010-4.48%2010-10-4.48-10-10-10z%22%2F%3E%3Cpath%20d%3D%22M412%20320c55.141%200%20100-44.86%20100-100s-44.859-100-100-100c-8.122%200-16.319%201.08-24.483%203.218C370.215%2052.119%20301.209%200%20226%200%20148.888%200%2078.951%2054.564%2063.528%20127.319%2025.29%20142.312%200%20178.836%200%20220c0%2055.14%2044.859%2080%2080%20100h146v52H136c-16.542%200-30%2013.458-30%2030v31.266c-17.232%204.452-30%2020.13-30%2038.734%200%2022.056%2017.944%2040%2040%2040s40-17.944%2040-40c0-18.604-12.768-34.282-30-38.734V402c0-5.514%204.486-10%2010-10h110v41.266c-17.232%204.452-30%2020.13-30%2038.734%200%2022.056%2017.944%2040%2040%2040s40-17.944%2040-40c0-18.604-12.768-34.282-30-38.734V392h110c5.514%200%2010%204.486%2010%2010v31.266c-17.232%204.452-30%2020.13-30%2038.734%200%2022.056%2017.944%2040%2040%2040s40-17.944%2040-40c0-18.604-12.768-34.282-30-38.734V402c0-16.542-13.458-30-30-30H266v-52h146zM136%20472c0%2011.028-8.972%2020-20%2020s-20-8.972-20-20%208.972-20%2020-20%2020%208.972%2020%2020zm280%200c0%2011.028-8.972%2020-20%2020s-20-8.972-20-20%208.972-20%2020-20%2020%208.972%2020%2020zm-140%200c0%2011.028-8.972%2020-20%2020s-20-8.972-20-20%208.972-20%2020-20%2020%208.972%2020%2020zM80%20300c-44.112%200-80-35.888-80-80%200-34.478%2022.255-64.896%2055.379-75.692.874-.285%201.69-.683%202.434-1.178%2027.287-7.868%2057.547-.907%2078.755%2020.301%203.906%203.905%2010.236%203.905%2014.143%200%203.905-3.905%203.905-10.237%200-14.143C151.823%20130.402%20126.711%20120%2080%20120c-4.775%200-9.518.353-14.205%201.021C103.412%2063.296%20162.07%2020%20226%2020c67.408%200%20128.42%2047.679%20142.535%20109.915-10.093%204.867-19.234%2011.362-27.246%2019.374-3.905%203.905-3.905%2010.237%200%2014.142%203.905%203.904%2010.237%203.906%2014.143%200C371.128%20147.732%20392.844%20140%20412%20140c44.112%200%2080%2035.888%2080%2080s-35.888%2080-80%2080H100z%22%2F%3E%3Cpath%20d%3D%22M309.829%2068.532C289.51%2051.2%20256.604%2040%20226%2040c-7.772%200-29.905%201.704-41.897%205.444-5.272%201.645-8.213%207.251-6.569%2012.524%201.645%205.272%207.252%208.212%2012.524%206.569C199.505%2061.59%20215.627%2060%20226%2060c25.725%200%2054.197%209.544%2070.851%2023.749%204.202%203.584%2010.514%203.082%2014.098-1.119%203.583-4.202%203.082-10.514-1.12-14.098z%22%2F%3E%3C%2Fsvg%3E')"
      }
    ]
  }
  const configObj = {
    timeOutEvent: 0,
    isMouseDown: false,
    torpData: {
      nodes: [],
      links: [],
      lines: [],
      text: []
    },
    initFlag: true,
    hoverFlag: false
  }

  const getXariaYaria = (limitNum, ariaType) => {
    // console.log('limitNum', limitNum)
    // console.log('ariaType', ariaType)
    let resaultNum = limitNum
    const key = ariaType === 'X' ? 'x' : 'y'
    const arr = configObj.torpData.nodes.filter((v) => { return v[key] > limitNum })
    if (arr.length > 0) {
      const rltArr = []
      arr.forEach((v) => {
        rltArr.push(v[key])
      })
      rltArr.sort((a, b) => { return a - b })
      // console.log('rltArr', rltArr)
      resaultNum = rltArr[rltArr.length - 1] + 100
    }
    // console.log('resaultNum', resaultNum)

    return resaultNum
  }
  // 初始化组件，渲染视窗元素
  this.init = () => {
    // 提示浏览器兼容，IE11以下提示兼容信息
    if ((navigator.userAgent.toLowerCase().indexOf('trident') > -1 && navigator.userAgent.toLowerCase().indexOf('trident/7.0') < 0) || navigator.userAgent.toLowerCase().indexOf('msie') > -1) {
      alert('您的浏览器版本过低，或不兼容本组件，请尝试使用新版chrome浏览器或火狐浏览器浏览～')
    }

    // 根据左中右视窗是否设置显示计算最后显示的视窗比例
    const _self = this
    const leftViewWidth = configObj.leftViewShow && configObj.couldEdit ? configObj.leftViewWidth : 0
    const centerViewWidth = configObj.centerViewShow ? configObj.centerViewWidth : 0
    const rightViewWidth = configObj.rightViewShow && configObj.couldEdit ? configObj.rightViewWidth : 0
    const widthAdd = computeViewWidth(leftViewWidth, centerViewWidth, rightViewWidth)
    const leftDiv = $('<div>').addClass('l000_view l000_left000_view').css({ 'width': (configObj.leftViewShow && configObj.couldEdit ? (leftViewWidth + widthAdd) / 24 * 100 : 0) + '%' }).hide().appendTo('#' + configObj.mainBoxId)
    const centerDiv = $('<div>').addClass('l000_view l000_opera000_view2').css({ 'width': (configObj.centerViewWidth + widthAdd) / 24 * 100 + '%' }).appendTo('#' + configObj.mainBoxId)
    const canvasDft = $('<canvas width="' + getXariaYaria(centerDiv.outerWidth(), 'X') + '" height="' + getXariaYaria(centerDiv.outerHeight(), 'Y') + '">').attr('id', configObj.canvasId).appendTo(centerDiv)
    const rightDiv = $('<div>').addClass('l000_view l000_right000_view').css({ 'width': (configObj.rightViewShow && configObj.couldEdit ? (rightViewWidth + widthAdd) / 24 * 100 : 0) + '%' }).hide().appendTo('#' + configObj.mainBoxId)
    const infoWindow = $('<div data-id=""></div>').addClass('l000_torp000_info000_window').appendTo(centerDiv)
    if (configObj.couldEdit) {
      // const inputButtonlabel = $('<button class="l000_inputButton">导入</button>').appendTo(centerDiv)
      const inputButton = $('<input type="file" id="l000_inputButton" style="opacity: 0;">').on('change', function() { handleFiles($(this)[0].files[0]) }).appendTo(centerDiv)
      const outputButton = $('<button id="l000_outputButton">导出</button>').on('click', () => { saveJSON(this.getTorpData(), false) }).appendTo(centerDiv)
      const innerLeft = new Promise((resolve, reject) => {
        if (configObj.leftViewShow) { leftDiv.show(); resolve() } else { leftDiv.hide() }
      }).then(() => {
        innerLeftView()
      })
      const innerRight = new Promise((resolve, reject) => {
        if (configObj.rightViewShow) { rightDiv.show(); resolve(this) } else { rightDiv.hide() }
      }).then(() => {
        innerRightView()
      })
    }
    if (configObj.onlyDrag) {
      // const saveButton = $('<button id="l000_outputButton">保存</button>').on('click', () => { saveJSON(this.getTorpData(), true) }).appendTo(centerDiv)
    }
    const innerCenter = new Promise((resolve, reject) => {
      if (configObj.centerViewShow) { centerDiv.show(); resolve(this) } else { centerDiv.hide() }
    }).then((_this) => {
      $('.l000_opera000_view2').on('mousemove', function(e) {
        $('.l000_torp000_info000_window').css(JSON.parse(computInfoWindowPosition(e)))
      })
      $('#' + configObj.canvasId).on('mousemove', (e) => {
        if ($('.l000_left000_active').length > 0 && $('.l000_left000_active').attr('data-type') === 'text') {
          $('#' + configObj.canvasId).css('cursor', 'text')
        } else {
          $('#' + configObj.canvasId).css('cursor', 'unset')
        }
        refreshCanvas($('#' + configObj.canvasId), e, false)
        if (configObj.hoverFlag) {
          if (configObj.onlyDrag) {
            $('#' + configObj.canvasId).addClass('l000_pointer')
          } else {
            $('.l000_torp000_info000_window').show()
          }
          configObj.hoverFlag = false
        } else {
          if (configObj.onlyDrag) {
            $('#' + configObj.canvasId).removeClass('l000_pointer')
          } else {
            $('.l000_torp000_info000_window').hide()
          }
        }
        // $('.l000_torp000_info000_window').css(JSON.parse(computInfoWindowPosition(e)))
      })
      $('#' + configObj.canvasId).off('mouseup').on('mouseup', (e) => {
        if ($('.l000_left000_active').length > 0) {
          const xNum = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true))
          const yNum = e.originalEvent.pageY - ($('.l000_opera000_view2').offset().top)
          let left = xNum
          let top = yNum
          left += $('.l000_opera000_view2').scrollLeft()
          top += $('.l000_opera000_view2').scrollTop()
          if ($('.l000_left000_active').attr('data-type') === 'text') {
            const id = new Date().getTime()
            const box = $('<div>').addClass('l000_torp000_element l000_left000_text').prop('id', 'l000_torp000_text000_' + id).css({ 'top': top, 'left': left }).appendTo('.l000_opera000_view2')
            const div = $('<div><span class="l000_text000_close">+</span><p class="l000_text000_area">自定义文本</p><input class="l000_text000_input" type="text" value="自定义文本"></div>').appendTo(box)
            configObj.torpData.text.push({ id: 'l000_torp000_text000_' + id, x: left, y: top, textValue: '自定义文本' })
            div.find('.l000_text000_close').on('click', function(e) {
              e.stopPropagation()
              const resaultArr = []
              configObj.torpData.text.forEach((v) => {
                if (v.id !== $(this).parents('.l000_left000_text').prop('id')) {
                  resaultArr.push(v)
                }
              })
              configObj.torpData.text = resaultArr
              $(this).parents('.l000_left000_text').remove()
            })
            div.find('.l000_text000_area').on('click', function(e) {
              e.stopPropagation()
              $(this).hide().siblings('input').show()
            })
            div.find('.l000_text000_input').on('input', function(e) {
              e.stopPropagation()
              $(this).siblings('p').text($(this).val())
            }).on('blur', function(e) {
              e.stopPropagation()
              e.preventDefault()
              if ($(this).val()) {
                configObj.torpData.text.forEach((v) => {
                  if (v.id === $(this).parents('.l000_left000_text').prop('id')) {
                    v.textValue = $(this).val()
                  }
                })
                $(this).hide().siblings('p').show()
              } else {
                const resaultArr = []
                configObj.torpData.text.forEach((v) => {
                  if (v.id !== $(this).parents('.l000_left000_text').prop('id')) {
                    resaultArr.push(v)
                  }
                })
                configObj.torpData.text = resaultArr
              }
            })
            div.hover(function() {
              $(this).css('background', 'rgba(83,173,255,0.6)').find('.l000_text000_close').show()
            }, function() {
              $(this).css('background', 'none').find('.l000_text000_close').hide()
            })
            changeBind(div)
            $('#' + configObj.canvasId).css('cursor', 'text')
            $('.l000_left000_active').removeClass('l000_left000_active')
          } else {
            if ($('.l000_left000_active').attr('data-type') === 'linear') {
              if (configObj.torpData.lines.length === 0 || configObj.torpData.lines[configObj.torpData.lines.length - 1].end) {
                configObj.torpData.lines.push({ id: 'l000_lines000_' + new Date().getTime(), start: { x: left, y: top }, end: null })
              } else if (configObj.torpData.lines[configObj.torpData.lines.length - 1].end === null) {
                if (Math.abs(left - configObj.torpData.lines[configObj.torpData.lines.length - 1].start.x) > Math.abs(top - configObj.torpData.lines[configObj.torpData.lines.length - 1].start.y)) {
                  top = configObj.torpData.lines[configObj.torpData.lines.length - 1].start.y
                } else {
                  left = configObj.torpData.lines[configObj.torpData.lines.length - 1].start.x
                }
                configObj.torpData.lines[configObj.torpData.lines.length - 1].end = { x: left, y: top }
              }
            } else {
              $('.l000_left000_active').removeClass('l000_left000_active')
            }
            $('#' + configObj.canvasId).css('cursor', 'unset')
          }
        }
        refreshCanvas($('#' + configObj.canvasId), e, true)
      })
    })
  }
  // 根据当前显示的视窗，计算隐藏的视窗多余宽度应分配给其它显示视窗多少比例
  const computeViewWidth = (l, c, r) => {
    let countNum = 0
    if (configObj.leftViewShow && configObj.couldEdit) countNum++
    if (configObj.centerViewShow) countNum++
    if (configObj.rightViewShow && configObj.couldEdit) countNum++
    return (24 - l - c - r) / countNum
  }
  // 合并配置项的方法
  const mergeObjectKey = (paramObj, baseObj) => {
    Object.keys(baseObj).forEach((v) => {
      if (paramObj[v] !== undefined && paramObj[v] !== null && Object.prototype.toString.call(baseObj[v]) === Object.prototype.toString.call(paramObj[v])) {
        configObj[v] = paramObj[v]
      } else {
        configObj[v] = baseObj[v]
      }
    })
  }
  // 渲染左侧视窗数据
  const innerLeftView = () => {
    $('.l000_left000_view').empty()
    const _self = this
    const elementul = $('<div class="l000_left000_drag000_box">' +
            '<h5 class="l000_title l000_open">拖拽元素</h5>' +
            '</div>').addClass('l000_form000_ul').appendTo('.l000_left000_view')
    const elementul2 = $('<div class="l000_left000_drag000_box">' +
            '<h5 class="l000_title l000_open">工具箱</h5>' +
            '<div class="l000_tool000_btn" data-type="linear">—</div>' +
            '<div class="l000_tool000_btn" data-type="text">T</div>' +
            '</div>').addClass('l000_form000_ul').appendTo('.l000_left000_view')
    configObj.elementType.forEach((v, i) => {
      const div = $('<div draggable="true"><p>' + v.name + '</p></div>').attr({ 'id': 'l000_drag000_id000_' + (i + 1), 'data-name': v.name, 'data-background-id': v.background000_id }).addClass('l000_drag000_able l000_drag000_element').css({ 'background': v.svg + ' #fff center no-repeat', 'background-size': '90% 90%' }).appendTo(elementul)
      addDragEvent(div)
    })
    addDropEvent($('.l000_opera000_view2'))
    /*$('.l000_tool000_btn').off('click').on('click', function(e) {
      if ($(this).hasClass('l000_left000_active')) {
        handleToolBtn(null, $(this).attr('data-type'))
        $(this).removeClass('l000_left000_active')
      } else {
        if ($('.l000_left000_active').length > 0) {
          handleToolBtn($(this).attr('data-type'), $('.l000_left000_active').attr('data-type'))
        } else {
          handleToolBtn($(this).attr('data-type'), null)
        }
        $('.l000_left000_active').removeClass('l000_left000_active')
        $(this).addClass('l000_left000_active')
      }
      if ($('.l000_left000_active').length === 0) {
        if (configObj.torpData.lines[configObj.torpData.lines.length - 1].end === null) {
          configObj.torpData.lines.pop()
          refreshCanvas($('#' + configObj.canvasId), e, false)
        }
      }
    })*/
  }
  // 处理工具栏点击事件方法
  const handleToolBtn = (clickEl, prevEl) => {
    // console.log(clickEl,prevEl)
    // if(clickEl){
    //     this['#start_'+clickEl]();
    // }
    // if(prevEl){
    //     this['#end_'+clickEl]();
    // }
  }
  // 渲染右侧视窗数据
  const innerRightView = () => {
    $('.l000_right000_view').empty()
    // 元素属性框初始化渲染及表单事件绑定
    const _self = this
    const elementBox = $('<div>').addClass('l000_element000_box l000_right000_box').hide().appendTo($('.l000_right000_view'))
    const elementul = $('<ul>' +
            '<h5 class="l000_title l000_open">基础属性</h5>' +
            '<li><label>元素名称：<input class="l000_element000_name" type="text" placeholder="请输入元素名称"></label></li>' +
            '<li><label>自定义ID：<input class="l000_element000_id" type="text" placeholder="请输入元素ID"></label></li>' +
            '<li><label>元素样式：<select class="l000_element000_style"><option value="-1">自定义样式</option></select></label></li>' +
            '<li class="l000_diy000_style"><label>自定义样式：</label><div><p>预览效果</p><span id="img_view"></span><input id="l000_img000_file" type="file"><b>选择文件</b></div></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(elementBox)
    configObj.elementType.forEach((v) => {
      const option = $('<option>').val(v.background_id).text(v.name)
      elementul.find('select.l000_element000_style').append(option)
    })
    elementul.find('input.l000_element000_name').off('input').on('input', function() {
      if ($('.l000_element000_box').attr('data-element-id')) {
        $('#' + $('.l000_element000_box').attr('data-element-id')).attr('data-name', $(this).val()).find('p').text($(this).val())
      }
    }).off('blur').on('blur', function() {
      const val = $(this).val()
      configObj.torpData.nodes.forEach((v) => {
        if (v.id === $('.l000_element000_box').attr('data-element-id')) {
          v.name = val
        }
      })
    })
    const elementul2 = $('<ul>' +
            '<h5 class="l000_title l000_open">自定义属性</h5>' +
            '<ul>参数格式：<br>{' +
            '<li class="l000_nomargin"> ' +
            '<p>“<span class="l000_key"></span>”:”<span class="l000_value"></span>”,</p>' +
            '</li>}' +
            '<li>html自定属性格式：<br> ' +
            '<p>data-torp-<span class="l000_data000_attr000_key"></span>=“<span class="l000_data000_attr000_value"></span>”</p>' +
            '</li>' +
            '</ul><br>' +
            '<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值"><span class="l000_delete000_diy000_style">+</span></li>' +
            '<li class="l000_add000_diy000_style"><p>新增自定义属性</p></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(elementBox)

    const lineBox = $('<div>').addClass('l000_line000_box l000_right000_box').hide().appendTo($('.l000_right000_view'))
    const lineul = $('<ul>' +
            '<h5 class="l000_title l000_open">基础属性</h5>' +
            '<li><label>线条ID：<input class="l000_line000_id" type="text" placeholder="请输入线条ID"></label></li>' +
            '<li><label>线条名称：<input class="l000_line000_name" type="text" placeholder="请输入线条名称"></label></li>' +
            '<li><label>线条样式：<select class="l000_line000_style"><option value="line">实线</option><option value="dash">虚线</option></select></label></li>' +
            '<li><label>箭头样式：<select class="l000_arrow000_style"><option value="single">单向箭头</option><option value="both">双向箭头</option><option value="none">无箭头</option></select></label></li>' +
            '<li><label>线条颜色：<select class="l000_line000_color"><option value="#53ADFF">#53ADFF</option><option value="#FF5D54">#FF5D54</option><option value="#17E572">#17E572</option><option value="-1">自定义颜色</option></select></label></li>' +
            '<li class="l000_diy000_color"><label>自定义颜色：</label><div><span id="l000_color"></span><input id="l000_color000_input" type="text" placeholder="请输入十六进制色码"></div></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(lineBox)
    elementul.find('select.l000_element000_style').empty()
    elementul.find('select.l000_element000_style').append($('<option value="-1">自定义样式</option>'))
    configObj.elementType.forEach((v) => {
      const option = $('<option>').val(v.background_id).text(v.name)
      elementul.find('select.l000_element000_style').append(option)
    })
    const lineul2 = $('<ul>' +
            '<h5 class="l000_title l000_open">自定义属性</h5>' +
            '<ul>参数格式：<br>{' +
            '<li class="l000_nomargin"> ' +
            '<p>“<span class="l000_key"></span>”:”<span class="l000_value"></span>”,</p>' +
            '</li>}' +
            '<li>html自定属性格式：<br> ' +
            '<p>data-torp-<span class="l000_data000_attr000_key"></span>=“<span class="l000_data000_attr000_value"></span>”</p>' +
            '</li>' +
            '</ul><br>' +
            '<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值"><span class="l000_delete000_diy000_style">+</span></li>' +
            '<li class="l000_add000_diy000_style"><p>新增自定义属性</p></li>' +
            '</ul>').addClass('l000_form000_ul').appendTo(lineBox)

    elementul2.find('input').on('input', function() {
      const liIdx = $(this).parent().index() - 3
      const iptIdx = $(this).index()
      const val = $(this).val()
      $(this).parents('ul.l000_form000_ul').find('li').each(function() {
        $(this).find('p').each(function(i) {
          if (i === liIdx) {
            $(this).find('span').eq(iptIdx).text(val)
          }
        })
      })
    }).on('blur', function(e) {
      e.preventDefault()
      if ($(this).parent().find('input').eq(0).val() == '') {
        $(this).parent().find('input').eq(0).val('diy000_attr000_' + new Date().getTime())
      } else {
        const idx = $(this).parent().index() - 3
        const val = $(this).parent().find('input').eq(0).val()
        let flag = true
        elementul2.find('li.l000_diy000_input000_box').each(function(i) {
          if (i !== idx && $(this).find('input').eq(0).val() === val) {
            flag = false
          }
        })
        if (flag) {
          updateDiyAttr('data-element-id', 'nodes', elementul2)
        } else {
          alert('自定义属性名不可以重复！')
          $(this).parent().find('input').eq(0).val('')
          const val2 = $(this).parent().find('input').eq(1).val()
          const idx = $(this).parent().index() - 3
          $(this).parent().siblings('ul').find('li').each(function() {
            $(this).find('p').each(function(i) {
              if (i === idx) {
                $(this).find('span').eq(0).text('')
                $(this).find('span').eq(1).text(val2)
              }
            })
          })
        }
      }
    })
    lineul2.find('input').on('input', function() {
      const liIdx = $(this).parent().index() - 3
      const iptIdx = $(this).index()
      const val = $(this).val()
      $(this).parents('ul.l000_form000_ul').find('li').each(function() {
        $(this).find('p').each(function(i) {
          if (i === liIdx) {
            $(this).find('span').eq(iptIdx).text(val)
          }
        })
      })
    }).on('blur', function(e) {
      e.preventDefault()
      if ($(this).parent().find('input').eq(0).val() == '') {
        $(this).parent().find('input').eq(0).val('diy000_attr000_' + new Date().getTime())
      } else {
        const idx = $(this).parent().index() - 3
        const val = $(this).parent().find('input').eq(0).val()
        let flag = true
        lineul2.find('li.l000_diy000_input000_box').each(function(i) {
          if (i !== idx && $(this).find('input').eq(0).val() === val) {
            flag = false
          }
        })
        if (flag) {
          updateDiyAttr('data-line-id', 'links', lineul2)
        } else {
          alert('自定义属性名不可以重复！')
          $(this).parent().find('input').eq(0).val('')
          const val2 = $(this).parent().find('input').eq(1).val()
          const idx = $(this).parent().index() - 3
          $(this).parent().siblings('ul').find('li').each(function() {
            $(this).find('p').each(function(i) {
              if (i === idx) {
                $(this).find('span').eq(0).text('')
                $(this).find('span').eq(1).text(val2)
              }
            })
          })
        }
      }
    })
    elementul2.find('.l000_delete000_diy000_style').on('click', function(e) {
      e.stopPropagation()
      e.preventDefault()
      if (elementul2.find('.l000_delete000_diy000_style').length < 2) {
        $(this).parent().find('input').eq(0).val('')
        $(this).parent().find('input').eq(1).val('')
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).find('span').eq(0).text('')
              $(this).find('span').eq(1).text('')
            }
          })
        })
      } else {
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).remove()
            }
          })
        })
        $(this).parent().remove()
      }
      updateDiyAttr('data-element-id', 'nodes', elementul2)
    })
    lineul2.find('.l000_delete000_diy000_style').on('click', function(e) {
      e.stopPropagation()
      e.preventDefault()
      if (lineul2.find('.l000_delete000_diy000_style').length < 2) {
        $(this).parent().find('input').eq(0).val('')
        $(this).parent().find('input').eq(1).val('')
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).find('span').eq(0).text('')
              $(this).find('span').eq(1).text('')
            }
          })
        })
      } else {
        const idx = $(this).parent().index() - 3
        $(this).parent().siblings('ul').find('li').each(function() {
          $(this).find('p').each(function(i) {
            if (i === idx) {
              $(this).remove()
            }
          })
        })
        $(this).parent().remove()
      }
      updateDiyAttr('data-line-id', 'links', lineul2)
    })
    $('.l000_element000_id').on('blur', function() {
      if ($(this).val() == '') {
        $(this).val('l000_torp000_' + new Date().getTime())
      }
      if ($(this).val() !== $(this).attr('data-old-id') && $('#' + $(this).val()).length === 0) {
        $('#' + $(this).attr('data-old-id')).prop('id', $(this).val())
        $('.l000_element000_box').attr('data-element-id', $(this).val())
        configObj.torpData.nodes.forEach((v) => {
          if (v.id === $(this).attr('data-old-id')) {
            v.id = $(this).val()
          }
        })
      } else {
        if ($('#' + $(this).val()).length > 0) {
          alert('自定义ID重复！')
          $(this).val('')
        }
      }
    })
    $('.l000_element000_name').on('blur', function() {
      configObj.torpData.nodes.forEach((v) => {
        if (v.id === $('.l000_element000_box').attr('data-element-id')) {
          v.name = $(this).val()
        }
      })
    })
    $('.l000_line000_name').on('blur', function() {
      configObj.torpData.links.forEach((v) => {
        if (v.id === $('.l000_line000_box').attr('data-line-id')) {
          v.name = $(this).val()
        }
      })
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    })
    $('#l000_color000_input').on('blur', function() {
      configObj.torpData.links.forEach((v) => {
        if (v.id === $('.l000_line000_box').attr('data-line-id')) {
          v.color = '#' + $(this).val()
          $('#l000_color').css('background', '#' + $(this).val())
        }
      })
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    })
    $('.l000_line000_id').on('blur', function() {
      let flag = true
      if ($(this).val() == '') {
        $(this).val('l000_line000_' + new Date().getTime())
      }
      configObj.torpData.links.forEach(function(v) {
        if ($(this).val() === v.id) {
          flag = false
        }
      })
      if ($(this).val() !== $(this).attr('data-old-id') && flag) {
        $('.l000_line000_box').attr('data-line-id', $(this).val())
        configObj.torpData.links.forEach((v) => {
          if (v.id === $(this).attr('data-old-id')) {
            v.id = $(this).val()
          }
        })
      } else {
        if (!flag) {
          alert('自定义ID重复！')
          $(this).val('')
        }
      }
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    })
    elementul.find('select.l000_element000_style').on('change', () => {
      if (elementBox.attr('data-element-id')) {
        if (elementul.find('select.l000_element000_style').val() == -1) {
          $('.l000_diy000_style').show()
        } else {
          $('.l000_diy000_style').hide()
          $('#l000_img000_file').val('')
          $('#img000_view').css('background', '#ccc')
        }
        configObj.torpData.nodes.forEach((v) => {
          if (v.id === $('.l000_element000_box').attr('data-element-id')) {
            v.background_id = $('.l000_element000_style').val()
            configObj.elementType.forEach((j) => {
              if (j.background_id === $('.l000_element000_style').val()) {
                v.background = j.svg
                $('#' + $('.l000_element000_box').attr('data-element-id')).attr('data-background-id', $('.l000_element000_style').val()).css({ 'background': j.svg + ' center no-repeat ', 'background-size': '90% 90%' })
              }
            })
          }
        })
      }
    })
    lineul.find('select.l000_line000_color').on('change', () => {
      if (lineBox.attr('data-line-id')) {
        if (lineul.find('select.l000_line000_color').val() == -1) {
          $('.l000_diy000_color').show()
        } else {
          $('.l000_diy000_color').hide()
          $('#l000_color000_input').val('')
          $('#l000_color').css('background', '#ccc')
        }
        configObj.torpData.links.forEach((v) => {
          if (v.id === $('.l000_line000_box').attr('data-line-id')) {
            if (lineul.find('select.l000_line000_color').val() == -1) {
              v.color = '#' + $('#l000_color000_input').val()
            } else {
              v.color = $('.l000_line000_color').val()
            }
          }
        })
        refreshCanvas($('#' + configObj.canvasId), undefined, false)
      }
    })
    lineul.find('select.l000_line000_style').on('change', () => {
      if (lineBox.attr('data-line-id')) {
        configObj.torpData.links.forEach((v) => {
          if (v.id === $('.l000_line000_box').attr('data-line-id')) {
            v.isDash = lineul.find('select.l000_line000_style').val() === 'dash'
          }
        })
        refreshCanvas($('#' + configObj.canvasId), undefined, false)
      }
    })
    lineul.find('select.l000_arrow000_style').on('change', () => {
      if (lineBox.attr('data-line-id')) {
        configObj.torpData.links.forEach((v) => {
          if (v.id === $('.l000_line000_box').attr('data-line-id')) {
            v.arrowType = lineul.find('select.l000_arrow000_style').val()
          }
        })
        refreshCanvas($('#' + configObj.canvasId), undefined, false)
      }
    })
    $('#l000_img000_file').on('change', () => {
      const fileType = $('#l000_img000_file').val().split('.')[$('#l000_img000_file').val().split('.').length - 1]
      if (fileType.toLowerCase() === 'png' || fileType.toLowerCase() === 'jpg' || fileType.toLowerCase() === 'jpeg') {
        var file = $('#l000_img000_file')[0].files[0]
        if (file.size / 1024 < 150) {
          var reader = new FileReader()
          reader.readAsDataURL(file) // 将文件读取为Data URL小文件   这里的小文件通常是指图像与 html 等格式的文件
          reader.onload = function(e) {
            $('#img_view').css({ 'background': 'url(' + e.target.result + ') center no-repeat ', 'background-size': '90% 90%' })
            // document.getElementById("img_z_base64").value = reader.result;
            $('#' + $('.l000_element000_box').attr('data-element-id')).attr('data-background-id', $('.l000_element000_style').val()).css({ 'background': 'url(' + e.target.result + ') center no-repeat ', 'background-size': '90% 90%' })
            configObj.torpData.nodes.forEach((v) => {
              if (v.id === $('.l000_element000_box').attr('data-element-id')) {
                v.background_id = '-1'
                v.background = 'url(' + e.target.result + ')'
              }
            })
          }
        } else {
          $('#l000_img000_file').val('')
          alert('请确保图片大小在150Kb以下')
        }
      } else {
        alert('请使用png或jpg格式文件上传')
      }
    })
    elementul2.find('.l000_add000_diy000_style').on('click', function(e) {
      const p1 = $(this).siblings('ul').find('li').eq(0).find('p').eq(0).clone(true)
      const p2 = $(this).siblings('ul').find('li').eq(1).find('p').eq(0).clone(true)
      const li = $(this).siblings('li.l000_diy000_input000_box').eq(0).clone(true)
      li.find('input').val('')
      p1.find('span').text('')
      p2.find('span').text('')
      p1.appendTo($(this).siblings('ul').find('li').eq(0))
      p2.appendTo($(this).siblings('ul').find('li').eq(1))
      $(this).before(li)
    })
    lineul2.find('.l000_add000_diy000_style').on('click', function(e) {
      const p1 = $(this).siblings('ul').find('li').eq(0).find('p').eq(0).clone(true)
      const p2 = $(this).siblings('ul').find('li').eq(1).find('p').eq(0).clone(true)
      const li = $(this).siblings('li.l000_diy000_input000_box').eq(0).clone(true)
      li.find('input').val('')
      p1.find('span').text('')
      p2.find('span').text('')
      p1.appendTo($(this).siblings('ul').find('li').eq(0))
      p2.appendTo($(this).siblings('ul').find('li').eq(1))
      $(this).before(li)
    })
    elementul.find('select.l000_element000_style').find('option').eq(0).appendTo(elementul.find('select.l000_element000_style'))
    elementul.find('select.l000_element000_style').val(elementul.find('select.l000_element000_style').find('option').eq(0).val()).change()

    // 线条属性框初始化渲染及表单事件绑定
    $('.l000_title').on('mouseup', function(e) {
      e.stopPropagation()
      e.preventDefault()
      if ($(this).hasClass('l000_open')) {
        $(this).parent().css('height', '1px')
      } else {
        $(this).parent().css('height', 'auto')
      }
      $(this).toggleClass('l000_open')
    })
  }
  // 添加拖拽事件监听
  const addDragEvent = (dragElement) => {
    dragElement.off('dragstart').on('dragstart', (e) => {
      e.dataTransfer = e.originalEvent.dataTransfer
      e.dataTransfer.setData('id', e.target.id)
      e.dataTransfer.setDragImage(e.target, 30, 30)
    })
  }
  // 添加拖拽事件监听
  const addDropEvent = (dropBox) => {
    dropBox.off('dragenter').on('dragenter', (e) => {
      e.preventDefault()
    })
    dropBox.off('dragover').on('dragover', (e) => {
      e.preventDefault()
      // drop.innerHTML = '';
    })
    dropBox.off('dragleave').on('dragleave', (e) => {
      e.preventDefault()
    })
    dropBox.off('drop').on('drop', (e) => {
      e.dataTransfer = e.originalEvent.dataTransfer || window.event.dataTransfer
      const targetId = e.dataTransfer.getData('id')
      const xNum = e.originalEvent.pageX - ($('#' + targetId).parent().offset().left + $('#' + targetId).parent().outerWidth(true) + 30);
      const yNum = e.originalEvent.pageY - ($('#' + targetId).parent().offset().top + 30);
      const left = xNum > 0 ? Math.floor(xNum) : 0
      const top = xNum > 0 ? Math.floor(yNum) : 0
      if ($('#' + targetId).hasClass('l000_drag000_able')) {
        const positionObj = computPosition({ left: left, top: top }, 10, undefined)
        const elBox = $('<div>').addClass('l000_torp000_element').css({ 'top': positionObj.top, 'left': positionObj.left }).appendTo(dropBox)
        const closeBtn = $('<div>+</div>').addClass('l000_del000_torp').appendTo(elBox)
        const id = 'l000_torp000_' + new Date().getTime()
        const background = 'url(' + $('#' + targetId).prop('style')['background'].split('url(')[1].split(')')[0] + ')'
        const div = $('#' + targetId).clone(true).prop({ 'id': id, 'draggable': false }).removeClass('l000_drag000_able').appendTo(elBox)
        configObj.torpData.nodes.push(
          {
            id: id,
            x: positionObj.left,
            y: positionObj.top,
            name: div.attr('data-name'),
            background_id: div.attr('data-background-id'),
            background: background,
            diy_attr: {}
          }
        )

        // 添加连线锚点方法
        addPoint(elBox)
        // 改变clone元素的绑定事件方法
        changeBind(div)
        closeBtn.on('click', (e) => {
          if (confirm('确认删除此元素吗？')) {
            $('.l000_right000_box').hide()
            $('#l000_img000_file').val('')
            $('#img000_view').css('background', '#ccc')

            elBox.remove()
            const afterDeleteNodeArr = []
            configObj.torpData.nodes.forEach((v) => {
              if (v.id !== div.prop('id')) {
                afterDeleteNodeArr.push(v)
              }
            })
            configObj.torpData.nodes = afterDeleteNodeArr
            const afterDeletePositionArr = []
            configObj.torpData.links.forEach((v) => {
              if (v.source.indexOf(div.prop('id').split('000_')[2]) < 0 && v.target.indexOf(div.prop('id').split('000_')[2]) < 0) {
                afterDeletePositionArr.push(v)
              }
            })
            configObj.torpData.links = afterDeletePositionArr
            refreshCanvas($('#' + configObj.canvasId), e, false)
          }
        })
      }
    })
  }
  // 对于已经生成的拓扑图元素转换绑定事件
  const changeBind = (element) => {
    // 解除绑定拖拽相关事件
    element.off('dragstart,drag,dragenter,dragover,dragleave,drop')
    element.parent().off('mousedown').on('mousedown', (e) => {
      e.stopPropagation()
      // e.preventDefault();
      configObj.isMouseDown = true
      configObj.timeOutEvent = setTimeout(() => { longPress() }, 500)
      element.parent().off('mousemove').on('mousemove', (e) => {
        e.stopPropagation()
        e.preventDefault()
        // 确保本次触发的mouseMove事件是通过当前元素的mouseDown触发的，以区分hover。
        if (configObj.isMouseDown) {
          // 因为统一用mouse事件操作，因此需要将timeOutEvent归零，用于区别用户的click和drag行为。
          clearTimeout(configObj.timeOutEvent)
          configObj.timeOutEvent = 0

          // 计算当前拖拽元素位置（包含已经出现的滚动条位移）
          let xNum = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true) + 50)
          let yNum = e.originalEvent.pageY - ($('.l000_opera000_view2').offset().top + 50)
          if ($(e.target).parents('.l000_torp000_element').hasClass('l000_left000_text')) {
            xNum -= 10
            yNum -= 10
          }
          let left = xNum
          let top = yNum
          left += $('.l000_opera000_view2').scrollLeft()
          top += $('.l000_opera000_view2').scrollTop()

          // 元素根据鼠标光标进行相应移动
          element.parent().css({ 'left': left, 'top': top })

          // 拖拽到操作区域右边缘和下边缘时，自动增加可拖拽区域面积(和canvas画布的height和width属性，确保canvas画布不变形)并将滚动条移动至相应区域
          const topLimit = $('#' + configObj.canvasId).outerHeight(true) - e.pageY + $('.l000_opera000_view2').offset().top - $('.l000_opera000_view2').scrollTop()
          const leftLimit = $('#' + configObj.canvasId).outerWidth(true) - e.pageX + $('.l000_opera000_view2').offset().left - $('.l000_opera000_view2').scrollLeft()
          if (topLimit < 30) {
            $('#' + configObj.canvasId).prop('height', $('#' + configObj.canvasId).outerHeight(true) + 10)
            $('.l000_opera000_view2').scrollTop($('.l000_opera000_view2').scrollTop() + 10)
          }
          if (leftLimit < 30) {
            $('#' + configObj.canvasId).prop('width', $('#' + configObj.canvasId).outerWidth(true) + 10)
            $('.l000_opera000_view2').scrollLeft($('.l000_opera000_view2').scrollLeft() + 10)
          }
          refreshCanvas($('#' + configObj.canvasId), e, false)
        }
      })
    }).off('mouseup').on('mouseup', (e) => {
      e.stopPropagation()
      e.preventDefault()
      configObj.isMouseDown = false
      element.parent().off('mousemove')
      clearTimeout(configObj.timeOutEvent)
      // 根据timeOutEvent判断是否为点击事件
      if (configObj.timeOutEvent != 0) {
        // 如果点击的是图标元素，则触发显示元素属性操作区功能
        if ($(e.target).prop('class').indexOf('l000_drag000_element') > -1) {
          $('.l000_element000_checked').removeClass('l000_element000_checked')
          $(e.target).addClass('l000_element000_checked')
          init_element_form('nodes', $(e.target))
          if (configObj.onlyDrag) {
            $('.l000_mask').fadeIn()
          }
        }
        // 如果点击的是锚点，则触发连线功能
        if ($(e.target).prop('class').indexOf('l000_torp000_dot') > -1) {
          link_line($('#' + configObj.canvasId), $(e.target))
        }
      } else {
        const positionObj = computPosition({ left: parseFloat($(e.target).parent().css('left').replace('px', '')), top: parseFloat($(e.target).parent().css('top').replace('px', '')) }, 10, $(e.target).parent())
        const left = positionObj.left
        const top = positionObj.top
        $(e.target).parent().css({ 'top': top, 'left': left })
        refreshCanvas($('#' + configObj.canvasId), e, false)
      }
    }).hover(() => {
      // element.parent().find('div.l000_del000_torp').show();
      // configObj.torpData.nodes.forEach((v)=>{
      //     if(v.id === element.prop('id')){
      //         $('.l000_torp000_info000_window').attr('data-id',v.id).empty();
      //         $('<p>元素ID：'+v.id+'</p>').appendTo('.l000_torp000_info000_window');
      //         $('<p>元素名称：'+v.name+'</p>').appendTo('.l000_torp000_info000_window');
      //         if(Object.keys(v.diy000_attr).length > 0){
      //             $('<p>自定义属性：{</p>').appendTo('.l000_torp000_info000_window');
      //             Object.keys(v.diy000_attr).forEach((j)=>{
      //                 $('<p style="text-indent: 20px;">'+j+':'+v.diy000_attr[j]+',</p>').appendTo('.l000_torp000_info000_window');
      //             });
      //             $('<p>}</p>').appendTo('.l000_torp000_info000_window');

      //         }
      //         $('.l000_torp000_info000_window').show();
      //     }
      // });
    }, () => {
      element.parent().find('div.l000_del000_torp').hide()
      $('.l000_torp000_info000_window').hide()
    })
  }
  // 计算连线方法
  const link_line = (canvasElement, targetElement) => {
    const dragId = targetElement.parent().find('div.l000_drag000_element').prop('id').split('l000_torp000_')[1]
    if (targetElement.hasClass('l000_dot000_active')) {
      configObj.torpData.links.pop()
      targetElement.removeClass('l000_dot000_active')
    } else {
      targetElement.addClass('l000_dot000_active')
    }
    if ($('.l000_dot000_active').length === 1) {
      const sourceClass = 'l000_' + targetElement.attr('data-position') + '000_' + dragId + '000_' + new Date().getTime()
      targetElement.addClass(sourceClass)
      configObj.torpData.links.push({ id: 'l000_line000_' + new Date().getTime(), name: '', source: sourceClass, target: null, color: '#53ADFF', isDash: false, arrowType: 'single', diy_attr: {}})
    }
    if ($('.l000_dot000_active').length === 2) {
      const targetClass = 'l000_' + targetElement.attr('data-position') + '000_' + dragId + '000_' + new Date().getTime()
      targetElement.addClass(targetClass)
      // 判断是否有重复连线
      if (hasLine(dragId)) {
        const sourceClass = configObj.torpData.links[configObj.torpData.links.length - 1]['source']
        alert('已有连线关系，请勿重复连线')
        targetElement.removeClass(targetClass)
        $('.' + sourceClass).removeClass(sourceClass)
        configObj.torpData.links.pop()
      } else {
        configObj.torpData.links[configObj.torpData.links.length - 1]['target'] = targetClass
      }
      // 连线完成，删除锚点选中样式
      $('.l000_dot000_active').removeClass('l000_dot000_active')
    }
  }
  // 刷新canvas画布方法
  const refreshCanvas = (element, e, ischeckClick) => {
    const canvas = element[0]
    const context = canvas.getContext('2d')
    context.clearRect(0, 0, canvas.width, canvas.height)
    if ($('.l000_torp000_element').length > 0) {
      // console.log('links', configObj.torpData.links)
      configObj.torpData.links.forEach((v, i) => {
        context.lineWidth = 2
        const startX = $('.' + v.source).offset().left - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true) - 6) + $('.l000_opera000_view2').scrollLeft()
        const startY = $('.' + v.source).offset().top - ($('.l000_opera000_view2').offset().top - 6) + $('.l000_opera000_view2').scrollTop()
        let endX
        let endY
        let x
        let y
        if (e) {
          x = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view2').scrollLeft()
          y = e.originalEvent.pageY - ($('.l000_opera000_view2').offset().top) + $('.l000_opera000_view2').scrollTop()
        } else {
          x = 0
          y = 0
        }
        if (v.target) {
          // console.log('555000', v.target)
          // console.log('666000', $('.' + v.target))
          // console.log('777000', $('#' + configObj.mainBoxId).offset().left)
          // console.log('888000', $('.l000_left000_view').outerWidth(true))

          // console.log('vvv!!!!!', v)
          // console.log('v.target!!!!!', v.target)
          // console.log('left!!!!!', $('.' + v.target))
          // console.log('configObj.mainBoxId!!!!!', $('.' + configObj.mainBoxId))
          // console.log('11222223', $('#' + configObj.mainBoxId).offset().left)
          // console.log('11222224', $('.l000_left000_view').outerWidth(true))
          // console.log('11222225', $('.l000_opera000_view').scrollLeft())
          endX = $('.' + v.target).offset().left - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true) - 6) + $('.l000_opera000_view2').scrollLeft()
          endY = $('.' + v.target).offset().top - ($('.l000_opera000_view2').offset().top - 6) + $('.l000_opera000_view2').scrollTop()
        } else {
          endX = (e ? e.originalEvent.pageX : 0) - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view2').scrollLeft()
          endY = (e ? e.originalEvent.pageY : 0) - ($('.l000_opera000_view2').offset().top) + $('.l000_opera000_view2').scrollTop()
        }
        drawArrow(canvas, context, { x: startX, y: startY }, { x: endX, y: endY }, x, y, ischeckClick, v.arrowType, v)
      })
    }
    if (configObj.torpData.lines.length > 0) {
      configObj.torpData.lines.forEach((v, i) => {
        context.lineWidth = 8
        const startX = v.start.x
        const startY = v.start.y
        let endX
        let endY
        let x
        let y
        if (e) {
          x = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view2').scrollLeft()
          y = e.originalEvent.pageY - ($('.l000_opera000_view2').offset().top) + $('.l000_opera000_view2').scrollTop()
        } else {
          x = 0
          y = 0
        }
        if (v.end) {
          endX = v.end.x
          endY = v.end.y
        } else {
          endX = (e ? e.originalEvent.pageX : 0) - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)) + $('.l000_opera000_view2').scrollLeft()
          endY = (e ? e.originalEvent.pageY : 0) - ($('.l000_opera000_view2').offset().top) + $('.l000_opera000_view2').scrollTop()
          if (Math.abs(endX - startX) > Math.abs(endY - startY)) {
            endY = startY
          } else {
            endX = startX
          }
        }
        drawArrow(canvas, context, { x: startX, y: startY }, { x: endX, y: endY }, x, y, ischeckClick, 'none', v)
      })
    }
  }
  // 长按操作判断
  const longPress = () => {
    configObj.timeOutEvent = 0
    // if(confirm('是否删除该元素？')){}
  }
  // 添加锚点方法
  const addPoint = (element) => {
    const point = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'top').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
    const point2 = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'right').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
    const point3 = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'bottom').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
    const point4 = $('<div>').addClass('l000_torp000_dot').attr('data-position', 'left').css({ 'top': '50%', 'left': '50%', 'margin-left': '-7px' }).on('mousedown,mousemove,mouseup', (e) => { e.stopPropagation(); e.preventDefault(); alert(1111) }).appendTo(element)
  }
  // 判断是否有重复连线方法
  const hasLine = (targetId) => {
    let result = false
    const sourceId = configObj.torpData.links[configObj.torpData.links.length - 1]['source'].split('000_')[2]
    configObj.torpData.links.forEach((v, i) => {
      if (i < configObj.torpData.links.length - 1) {
        if ((v.source.indexOf(targetId) > -1 && v.target.indexOf(sourceId) > -1) || (v.source.indexOf(sourceId) > -1 && v.target.indexOf(targetId) > -1)) {
          result = true
        }
      }
    })
    return result
  }
  // 绘制箭头样式方法
  const drawArrow = (canvas, context, start, end, mouseX, mouseY, ischeckClick, arrowType, dataObj) => {
    // 计算两点距离，主要是为了计算斜率
    let distanceX = end.x - start.x, distanceY = end.y - start.y
    const distance = Math.sqrt(distanceY * distanceY + distanceX * distanceX)
    // 箭头的尺寸
    let distanceArrowType = 15, sharpeArrowType = 7
    // 先确定轴线与三角两个尖角点交汇坐标
    const arrowTypeMoveTo = {
      x: start.x + distanceArrowType * distanceX / distance,
      y: start.y + distanceArrowType * distanceY / distance
    }
    const arrowTypeLineTo = {
      x: end.x - distanceArrowType * distanceX / distance,
      y: end.y - distanceArrowType * distanceY / distance
    }
    // 4个对称点坐标
    const arrowTypeTo1 = {
      x: arrowTypeMoveTo.x - sharpeArrowType * distanceY / distance,
      y: arrowTypeMoveTo.y + sharpeArrowType * distanceX / distance
    }
    const arrowTypeTo2 = {
      x: arrowTypeMoveTo.x + sharpeArrowType * distanceY / distance,
      y: arrowTypeMoveTo.y - sharpeArrowType * distanceX / distance
    }
    const arrowTypeTo3 = {
      x: arrowTypeLineTo.x - sharpeArrowType * distanceY / distance,
      y: arrowTypeLineTo.y + sharpeArrowType * distanceX / distance
    }
    const arrowTypeTo4 = {
      x: arrowTypeLineTo.x + sharpeArrowType * distanceY / distance,
      y: arrowTypeLineTo.y - sharpeArrowType * distanceX / distance
    }
    arrowType = arrowType || 'single'
    if (dataObj.isDash) {
      context.setLineDash([5, 10])
    } else {
      context.setLineDash([])
    }
    // 开始绘制
    context.beginPath()
    // 三种箭头类型
    switch (arrowType) {
      case 'single': {
        context.moveTo(start.x, start.y)
        context.lineTo(end.x, end.y)
        // 两个结束对称点
        context.lineTo(arrowTypeTo3.x, arrowTypeTo3.y)
        context.lineTo(arrowTypeTo4.x, arrowTypeTo4.y)
        // 回到结束点
        context.lineTo(end.x, end.y)
        break
      }
      case 'both': {
        context.moveTo(start.x, start.y)
        // 两个起始对称点
        context.lineTo(arrowTypeTo1.x, arrowTypeTo1.y)
        context.lineTo(arrowTypeTo2.x, arrowTypeTo2.y)
        // 回到起始点
        context.lineTo(start.x, start.y)
        // 重复single的绘制
        context.lineTo(end.x, end.y)
        context.lineTo(arrowTypeTo3.x, arrowTypeTo3.y)
        context.lineTo(arrowTypeTo4.x, arrowTypeTo4.y)
        context.lineTo(end.x, end.y)
        break
      }
      case 'none': {
        context.moveTo(start.x, start.y)
        context.lineTo(end.x, end.y)
        break
      }
    }

    // 闭合，描边与填充
    context.closePath()
    // console.log('context123', JSON.stringify(context))
    if (context.isPointInPath(mouseX, mouseY) || context.isPointInStroke(mouseX, mouseY)) {
    //   console.log('dataObj123', JSON.stringify(dataObj))
      if (dataObj.id.split('000_')[1] === 'lines') {
        // if($('.l000_left000_active').attr('data-type') === 'linear'){
        //     if(ischeckClick && confirm('确认删除此线段吗？')){
        //         let rsaultArr = [];
        //         configObj.torpData.lines.forEach((v)=>{
        //             if(v.id !== dataObj.id){
        //                 rsaultArr.push(v);
        //             }
        //         });
        //         configObj.torpData.lines = rsaultArr;
        //     }
        // }
      } else if (dataObj.id.split('000_')[1] === 'line') {
        $('.connection_status').text('')
        $('.link_bandwidth').text('')
        $('.link_used').text('')
        $('.source_if_ip').text('')
        $('.source_if_port_channel').text('')
        $('.select_value').empty()
        var after_value_array = []
        var before_value_array = []
        if (ischeckClick) {
          init_element_form('lines', dataObj)
          if (configObj.onlyDrag) {
            $('.l000_win h5').text('链接信息')
            const source_both = dataObj.source.split('000_')[2]
            const target_both = dataObj.target.split('000_')[2]
            for (const iterator of dataObj.diy_attr.all_data.topology[0]['link']) {
              if ((iterator.source['source-node'] === source_both && iterator.destination['dest-node'] === target_both)) {
                // $('.select_value').empty()
                // console.log('??????????111111', iterator.source['source-tp'], iterator.destination['dest-tp'])
                $('.select_value').append("<option value='" + iterator.source['source-tp'] + "'>" + iterator.source['source-tp'] + '</option>')
                after_value_array.push(iterator.destination['dest-tp'])
                before_value_array.push(iterator.source['source-tp'])
              } else if ((iterator.source['source-node'] === target_both && iterator.destination['dest-node'] === source_both)) {
                // console.log('??????????222222', iterator.source['source-tp'], iterator.destination['dest-tp'])
                $('.select_value').append("<option value='" + iterator.source['source-tp'] + "'>" + iterator.source['source-tp'] + '</option>')
                after_value_array.push(iterator.destination['dest-tp'])
                before_value_array.push(iterator.source['source-tp'])
              }

              $('.after_value').text(after_value_array[0])
              // console.log('7777778', $('.select_value').val())
            }
            dataObj.diy_attr.all_data.topology[0]['link'].forEach(element => {
              if (element.source['source-tp'] === before_value_array[0] && element.destination['dest-tp'] === after_value_array[0]) {
                // console.log('qqq123', element['bandwidth'])
                // console.log('333', element['bandwidth-used'])
                // console.log('333444', element['status'])
                if (element.hasOwnProperty('bandwidth')) {
                  $('.link_bandwidth').text(element['bandwidth'])
                } else {
                  $('.link_bandwidth').text('')
                }
                if (element.hasOwnProperty('bandwidth-used')) {
                  $('.link_used').text(element['bandwidth-used'])
                } else {
                  $('.link_used').text('')
                }
                if (element['status'] === 'Connected') {
                  $('.connection_status').text('正常')
                } else {
                  $('.connection_status').text('异常')
                }
                if (element.hasOwnProperty('source-if-ip')) {
                  $('.source_if_ip').text(element['source-if-ip'])
                } else {
                  $('.source_if_ip').text('')
                }
                if (element.hasOwnProperty('source-if-port-channel')) {
                  $('.source_if_port_channel').text(element['source-if-port-channel'])
                } else {
                  $('.source_if_port_channel').text('')
                }
              }
            })
            // console.log('66668888', before_value_array)
            // console.log('77778888', before_value_array.length)
            // console.log('66668888', after_value_array)
            // console.log('77778888', after_value_array.length)
            // 图标双向单向
            // if (dataObj.arrowType === 'single') {
            //   $('.select_value').append("<option value='" + dataObj.diy_attr['link-id'] + "'>" + dataObj.diy_attr['link-id'] + '</option>')
            // } else if (dataObj.arrowType === 'both') {
            //   const source_both = dataObj.source.split('000_')[2]
            //   const target_both = dataObj.target.split('000_')[2]
            //   console.log('1', source_both)
            //   console.log('2', target_both)
            //   for (const iterator of dataObj.diy_attr.all_data.topology[0]['link']) {
            //     console.log('3', iterator.source['source-node'])
            //     console.log('4', iterator.destination['dest-node'])
            //     if ((iterator.source['source-node'] === source_both && iterator.destination['dest-node'] === target_both)) {
            //       console.log('??????????111111', iterator.source['source-tp'], iterator.destination['dest-tp'])
            //       $('.select_value').append("<option value='" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + "'>" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + '</option>')
            //     } else if ((iterator.source['source-node'] === target_both && iterator.destination['dest-node'] === source_both)) {
            //       console.log('??????????222222', iterator.source['source-tp'], iterator.destination['dest-tp'])
            //       $('.select_value').append("<option value='" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + "'>" + iterator.source['source-tp'] + '->' + iterator.destination['dest-tp'] + '</option>')
            //     }
            //   }
            // }
            // console.log('777777', $('.select_value').val())
            var arg_init = ''
            arg_init = $('.select_value').val().split('::')[0]
            const source_tp_init = $('.select_value').val().split('::')[1]
            var host_arg_init = ''
            for (const iteratorArg of dataObj.diy_attr.all_data.topology[0]['node']) {
              // console.log('00011', iteratorArg['node-id'])
              // console.log('00012', arg_init)
              var arg_init_2 = arg_init
              const reg = new RegExp('\\.', 'g')
              arg_init_2 = arg_init_2.replace(reg, '-')
              const reg2 = new RegExp(':', 'g')
              arg_init_2 = arg_init_2.replace(reg2, '-')
              if (iteratorArg['node-id'] === arg_init_2) {
                host_arg_init = iteratorArg['host']
              }
            }
            var bol_value = false
            var source_tp = ''
            var host_arg = ''
            var arg = ''
            $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg_init + '&var-Device=' + host_arg_init + '&var-Interface=' + source_tp_init + '&refresh=30s&kiosk')
            $('.select_value').change(function() {
              bol_value = true
              const str = ''
              // $('.select_value option:selected').each(function() {
              //   str = $(this).text()
              // })
              // console.log('str444', str)
              // console.log('before_value_array444', before_value_array)
              const before_index = $('option:selected', '.select_value').index()
              // console.log('before_index666', before_index)
              $('.after_value').text(after_value_array[before_index])
              arg = $(this).val().split('::')[0]
              source_tp = $(this).val().split('::')[1]
              for (const iteratorArg of dataObj.diy_attr.all_data.topology[0]['node']) {
                const reg = new RegExp('\\.', 'g')
                arg = arg.replace(reg, '-')
                const reg2 = new RegExp(':', 'g')
                arg = arg.replace(reg2, '-')
                // console.log('oooo', iteratorArg['node-id'])
                // console.log('ooooarg123', arg)
                if (iteratorArg['node-id'] === arg) {
                  host_arg = iteratorArg['host']
                }
              }
              // console.log('00000', $(this).val())
              // console.log('11111', after_value_array[before_index])
              dataObj.diy_attr.all_data.topology[0]['link'].forEach(element => {
                if (element.source['source-tp'] === $(this).val() && element.destination['dest-tp'] === after_value_array[before_index]) {
                  // console.log('222', element['bandwidth'])
                  // console.log('333', element['bandwidth-used'])
                  if (element.hasOwnProperty('bandwidth')) {
                    $('.link_bandwidth').text(element['bandwidth'])
                  } else {
                    $('.link_bandwidth').text('')
                  }
                  if (element.hasOwnProperty('bandwidth-used')) {
                    $('.link_used').text(element['bandwidth-used'])
                  } else {
                    $('.link_used').text('')
                  }
                  if (element['status'] === 'Connected') {
                    $('.connection_status').text('正常')
                  } else {
                    $('.connection_status').text('异常')
                  }
                  if (element.hasOwnProperty('source-if-ip')) {
                    $('.source_if_ip').text(element['source-if-ip'])
                  } else {
                    $('.source_if_ip').text('')
                  }
                  if (element.hasOwnProperty('source-if-port-channel')) {
                    $('.source_if_port_channel').text(element['source-if-port-channel'])
                  } else {
                    $('.source_if_port_channel').text('')
                  }
                }
              })
              // console.log('host_arg123', host_arg)
              // console.log('source_tp123', source_tp)
              // console.log('host_arg123444444', dataObj.diy_attr['bandwidth'])
              // console.log('source_tp12344444', dataObj.diy_attr)

              $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg + '&var-Device=' + host_arg + '&var-Interface=' + source_tp + '&refresh=30s&kiosk')
            })
            $('.btn_reset').click(function() {
              // console.log('bol_value123', bol_value)
              // console.log('host_arg_init', host_arg_init)
              // console.log('source_tp_init', source_tp_init)
              // console.log('host_arg', host_arg)
              // console.log('source_tp', source_tp)
              $('.monitoring_iframe').prop('src', '')
              if (bol_value === false) {
                $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg_init + '&var-Device=' + host_arg_init + '&var-Interface=' + source_tp_init + '&refresh=30s&kiosk')
              } else if (bol_value === true) {
                $('.monitoring_iframe').prop('src', 'http://198.218.6.36:3000/d/logview/logview?orgId=1&from=now-24h&to=now&var-Hostname=' + arg + '&var-Device=' + host_arg + '&var-Interface=' + source_tp + '&refresh=30s&kiosk')
              }
            })
            // $('#l000_link000_info').show()
            // $('#l000_mach000_info').hide()
            $('.l000_win').show()
            $('.l000_win_device').hide()
            $('.l000_mask').fadeIn()
          }
        }
        $('.l000_torp000_info000_window').attr('data-id', dataObj.id).empty()
        $('<p>元素ID：' + dataObj.id + '</p>').appendTo('.l000_torp000_info000_window')
        $('<p>元素名称：' + dataObj.name + '</p>').appendTo('.l000_torp000_info000_window')
        if (Object.keys(dataObj.diy_attr).length > 0) {
          $('<p>自定义属性：{</p>').appendTo('.l000_torp000_info000_window')
          Object.keys(dataObj.diy_attr).forEach((v) => {
            $('<p style="text-indent: 20px;">' + v + ':' + dataObj.diy_attr[v] + ',</p>').appendTo('.l000_torp000_info000_window')
          })
          $('<p>}</p>').appendTo('.l000_torp000_info000_window')
        }

        configObj.hoverFlag = true
      }
      context.fillStyle = '#3d7fbb'
      context.strokeStyle = '#44dcd7'
	  context.lineWidth=4
    } else {
      context.fillStyle = dataObj.color
      context.strokeStyle = dataObj.color
    }
    context.stroke()
    context.fill()
  }
  // 根据元素点击事件，渲染右侧属性表单
  const init_element_form = (type, dataObj) => {
    const _self = this
    if (type === 'lines') {
      let colorFlag = false
      $('.l000_line000_box').find('li.l000_diy000_li').remove()
      $('.l000_line000_id').val(dataObj.id).attr('data-old-id', dataObj.id)
      $('.l000_line000_name').val(dataObj.name)
      $('.l000_line000_style').val(dataObj.isDash ? 'dash' : 'line')
      $('.l000_arrow000_style').val(dataObj.arrowType)
      $('.l000_line000_color option').each(function() {
        if ($(this).val() === dataObj.color) {
          colorFlag = true
        }
      })
      if (colorFlag) {
        $('.l000_line000_color').val(dataObj.color)
        $('.l000_diy000_color').hide()
      } else {
        $('.l000_line000_color').val('-1')
        $('#l000_color000_input').val(dataObj.color.replace('#', ''))
        $('#l000_color').css('background', dataObj.color)
        $('.l000_diy000_color').show()
      }
      $('.l000_line000_box').attr('data-line-id', dataObj.id).show()
      $('.l000_element000_box').hide()

      configObj.torpData.links.forEach((v) => {
        if (v.id === dataObj.id) {
          $('.l000_line000_box').find('.l000_nomargin').find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          $('.l000_line000_box').find('li.l000_diy000_input000_box').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('input').val('')
            }
          })
          $('.l000_line000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          configObj.torpData.links.forEach((v) => {
            if (v.id === dataObj.id) {
              if (Object.keys(v.diy_attr).length > 0) {
                Object.keys(v.diy_attr).forEach((j) => {
                  const diy_ipt = $('<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名" value="' + j + '">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值" value="' + v.diy_attr[j] + '"><span class="l000_delete000_diy000_style">+</span></li>')
                  const diyAttr = $('<p>“<span class="l000_key">' + j + '</span>”:”<span class="l000_value">' + v.diy_attr[j] + '</span>”,</p>')
                  const diyHtmlAttr = $('<p>data-torp-<span class="l000_data000_attr000_key">' + j + '</span>=“<span class="l000_data000_attr000_value">' + v.diy_attr[j] + '</span>”</p>')
                  $('.l000_line000_box').find('.l000_add000_diy000_style').before(diy_ipt)
                  $('.l000_line000_box').find('.l000_nomargin').append(diyAttr)
                  $('.l000_line000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).append(diyHtmlAttr)
                  diy_ipt.find('input').on('input', function() {
                    const liIdx = $(this).parent().index() - 3
                    const iptIdx = $(this).index()
                    const val = $(this).val()
                    $(this).parents('ul.l000_form000_ul').find('li').each(function() {
                      $(this).find('p').each(function(i) {
                        if (i === liIdx) {
                          $(this).find('span').eq(iptIdx).text(val)
                        }
                      })
                    })
                  }).on('blur', function(e) {
                    e.preventDefault()
                    if ($(this).parent().find('input').eq(0).val() == '') {
                      $(this).parent().find('input').eq(0).val('diy_attr_' + new Date().getTime())
                    } else {
                      const idx = $(this).parent().index() - 3
                      const val = $(this).parent().find('input').eq(0).val()
                      let flag = true
                      diy_ipt.parent().find('li.l000_diy000_input000_box').each(function(i) {
                        if (i !== idx && $(this).find('input').eq(0).val() === val) {
                          flag = false
                        }
                      })
                      if (flag) {
                        updateDiyAttr('data-line-id', 'links', diy_ipt.parent())
                      } else {
                        alert('自定义属性名不可以重复！')
                        $(this).parent().find('input').eq(0).val('')
                        const val2 = $(this).parent().find('input').eq(1).val()
                        const idx = $(this).parent().index() - 3
                        $(this).parent().siblings('ul').find('li').each(function() {
                          $(this).find('p').each(function(i) {
                            if (i === idx) {
                              $(this).find('span').eq(0).text('')
                              $(this).find('span').eq(1).text(val2)
                            }
                          })
                        })
                      }
                    }
                  })
                  diy_ipt.find('.l000_delete000_diy000_style').on('click', function(e) {
                    e.stopPropagation()
                    e.preventDefault()
                    if (diy_ipt.parent().find('.l000_delete000_diy000_style').length < 2) {
                      $(this).parent().find('input').eq(0).val('')
                      $(this).parent().find('input').eq(1).val('')
                      const idx = $(this).parent().index() - 3
                      $(this).parent().siblings('ul').find('li').each(function() {
                        $(this).find('p').each(function(i) {
                          if (i === idx) {
                            $(this).find('span').eq(0).text('')
                            $(this).find('span').eq(1).text('')
                          }
                        })
                      })
                    } else {
                      const idx = $(this).parent().index() - 3
                      $(this).parent().siblings('ul').find('li').each(function() {
                        $(this).find('p').each(function(i) {
                          if (i === idx) {
                            $(this).remove()
                          }
                        })
                      })
                      $(this).parent().remove()
                    }
                    updateDiyAttr('data-line-id', 'links', diy_ipt.parent())
                  })
                })
              }
            }
          })
        }
      })
    }
    if (type === 'nodes') {
      $('.l000_line000_box').attr('data-line-id', '').hide()
      $('.l000_element000_name').val(dataObj.attr('data-name'))
      $('.l000_element000_id').attr('data-old-id', dataObj.prop('id')).val(dataObj.prop('id'))
      $('.l000_element000_box').find('li.l000_diy000_li').remove()
      $('.l000_element000_box').attr('data-element-id', dataObj.prop('id')).show()
      $('.l000_element000_style').val(dataObj.attr('data-background-id')).change()

      configObj.torpData.nodes.forEach((v) => {
        if (v.id === dataObj.prop('id')) {
          $('.l000_element000_box').find('.l000_nomargin').find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          $('.l000_element000_box').find('li.l000_dify000_input000_box').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('input').val('')
            }
          })
          $('.l000_element000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).find('p').each(function(i) {
            if (i > ((Object.keys(v.diy_attr).length > 0) ? -1 : 0)) {
              $(this).remove()
            } else {
              $(this).find('span').text('')
            }
          })
          if (Object.keys(v.diy_attr).length > 0) {
            Object.keys(v.diy_attr).forEach((j) => {
              const diy_ipt = $('<li class="l000_diy000_input000_box"><input type="text" data-class="key" placeholder="英文属性名" value="' + j + '">&nbsp;:&nbsp;<input type="text" data-class="value" placeholder="属性值" value="' + v.diy_attr[j] + '"><span class="l000_delete000_diy000_style">+</span></li>')
              const diyAttr = $('<p>“<span class="l000_key">' + j + '</span>”:”<span class="l000_value">' + v.diy_attr[j] + '</span>”,</p>')
              const diyHtmlAttr = $('<p>data-torp-<span class="l000_data000_attr000_key">' + j + '</span>=“<span class="l000_data000_attr000_value">' + v.diy_attr[j] + '</span>”</p>')
              $('.l000_element000_box').find('.l000_add000_diy000_style').before(diy_ipt)
              $('.l000_element000_box').find('.l000_nomargin').append(diyAttr)
              $('.l000_element000_box').find('ul.l000_form000_ul').eq(1).find('ul').find('li').eq(1).append(diyHtmlAttr)
              diy_ipt.find('input').on('input', function() {
                const liIdx = $(this).parent().index() - 3
                const iptIdx = $(this).index()
                const val = $(this).val()
                $(this).parents('ul.l000_form000_ul').find('li').each(function() {
                  $(this).find('p').each(function(i) {
                    if (i === liIdx) {
                      $(this).find('span').eq(iptIdx).text(val)
                    }
                  })
                })
              }).on('blur', function(e) {
                e.preventDefault()
                if ($(this).parent().find('input').eq(0).val() == '') {
                  $(this).parent().find('input').eq(0).val('diy_attr_' + new Date().getTime())
                } else {
                  const idx = $(this).parent().index() - 3
                  const val = $(this).parent().find('input').eq(0).val()
                  let flag = true
                  diy_ipt.parent().find('li.l000_diy000_input000_box').each(function(i) {
                    if (i !== idx && $(this).find('input').eq(0).val() === val) {
                      flag = false
                    }
                  })
                  if (flag) {
                    updateDiyAttr('data-element-id', 'nodes', diy_ipt.parent())
                  } else {
                    alert('自定义属性名不可以重复！')
                    $(this).parent().find('input').eq(0).val('')
                    const val2 = $(this).parent().find('input').eq(1).val()
                    const idx = $(this).parent().index() - 3
                    $(this).parent().siblings('ul').find('li').each(function() {
                      $(this).find('p').each(function(i) {
                        if (i === idx) {
                          $(this).find('span').eq(0).text('')
                          $(this).find('span').eq(1).text(val2)
                        }
                      })
                    })
                  }
                }
              })
              diy_ipt.find('.l000_delete000_diy000_style').on('click', function(e) {
                e.stopPropagation()
                e.preventDefault()
                if (diy_ipt.parent().find('.l000_delete000_diy000_style').length < 2) {
                  $(this).parent().find('input').eq(0).val('')
                  $(this).parent().find('input').eq(1).val('')
                  const idx = $(this).parent().index() - 3
                  $(this).parent().siblings('ul').find('li').each(function() {
                    $(this).find('p').each(function(i) {
                      if (i === idx) {
                        $(this).find('span').eq(0).text('')
                        $(this).find('span').eq(1).text('')
                      }
                    })
                  })
                } else {
                  const idx = $(this).parent().index() - 3
                  $(this).parent().siblings('ul').find('li').each(function() {
                    $(this).find('p').each(function(i) {
                      if (i === idx) {
                        $(this).remove()
                      }
                    })
                  })
                  $(this).parent().remove()
                }
                updateDiyAttr('data-element-id', 'nodes', diy_ipt.parent())
              })
            })
          }
        }
      })
    }
  }
  // 导出json文件方法
  const saveJSON = (data, sendAxios, filename) => {
    if (!data) {
      alert('保存的数据为空')
      return
    }
    if (sendAxios) {
      alert('此处发送请求保存数据的接口')
    } else {
      if (!filename) { filename = 'json.json' }
      if (typeof data === 'object') {
        data = JSON.stringify(data, undefined, 4)
      }
      let blob = new Blob([data], { type: 'text/json' }),
        e = document.createEvent('MouseEvents'),
        a = document.createElement('a')
      a.download = filename
      a.href = window.URL.createObjectURL(blob)
      a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
      e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
      a.dispatchEvent(e)
    }
  }
  // 读取文件方法
  const handleFiles = function(selectedFile) {
    if (selectedFile) {
      const _self = this
      var reader = new FileReader()
      reader.readAsText(selectedFile)// 读取文件的内容
      reader.onload = function() {
        const json = JSON.parse(this.result)
        if (Object.prototype.toString.call(json.nodes) === '[object Array]' && Object.prototype.toString.call(json.links) === '[object Array]' && Object.prototype.toString.call(json.lines) === '[object Array]' && Object.prototype.toString.call(json.text) === '[object Array]') {
          configObj.torpData = json
          $('#' + configObj.mainBoxId).empty()
          _self.init.call(_self)
          json.nodes.forEach((v) => {
            const elBox = $('<div>').addClass('l000_torp000_element').css({ 'top': v.y + 'px', 'left': v.x + 'px' }).appendTo($('.l000_opera000_view2'))
            const closeBtn = $('<div>+</div>').addClass('l000_del000_torp').appendTo(elBox)
            const div = $('<div><p>' + v.name + '</p></div>').attr({ 'id': v.id, 'data-name': v.name, 'data-background-id': v.background_id }).addClass('l000_drag000_element').css({ 'background': v.background + ' #fff center no-repeat', 'background-size': '100% 100%' }).appendTo(elBox)
            // 添加连线锚点方法
            addPoint(elBox)
            // 改变clone元素的绑定事件方法
            changeBind(div)
            closeBtn.on('click', (e) => {
              if (confirm('确认删除此元素吗？')) {
                $('.l000_right000_box').hide()
                $('#l000_img000_file').val('')
                $('#img_view').css('background', '#ccc')

                elBox.remove()
                const afterDeleteNodeArr = []
                configObj.torpData.nodes.forEach((v) => {
                  if (v.id !== div.prop('id')) {
                    afterDeleteNodeArr.push(v)
                  }
                })
                configObj.torpData.nodes = afterDeleteNodeArr
                const afterDeletePositionArr = []
                configObj.torpData.links.forEach((v) => {
                  if (v.source.indexOf(div.prop('id').split('000_')[2]) < 0 && v.target.indexOf(div.prop('id').split('000_')[2]) < 0) {
                    afterDeletePositionArr.push(v)
                  }
                })
                configObj.torpData.links = afterDeletePositionArr
                refreshCanvas($('#' + configObj.canvasId), e, false)
              }
            })
          })
          json.links.forEach((v) => {
            addDotClass(v.source)
            addDotClass(v.target)
          })
          refreshCanvas($('#' + configObj.canvasId), undefined, false)
        } else {
          alert('导入文件的数据格式不正确！')
        }
      }
    }
  }
  // 添加锚点class
  const addDotClass = (val) => {
    $('#l000_torp000_' + val.split('000_')[2]).parent().find('.l000_torp000_dot').each(function() {
      if ($(this).attr('data-position') === val.split('000_')[1]) {
        $(this).addClass(val)
      }
    })
  }
  // 更新自定义属性
  const updateDiyAttr = (attr, key, template) => {
    configObj.torpData[key].forEach((v) => {
      if (v.id === template.parent().attr(attr)) {
        v.diy_attr = {}
        template.find('li.l000_diy000_input000_box').each(function() {
          v.diy_attr[$(this).find('input').eq(0).val()] = $(this).find('input').eq(1).val()
        })
      }
    })
  }
  // 计算位置重叠方法
  const computPosition = (posotion, num, el) => {
    let count = 0;
    (el ? el.siblings('.l000_torp000_element') : $('.l000_torp000_element')).each(function() {
      const inX = parseFloat($(this).css('left').replace('px', '')) < (posotion.left + num) && parseFloat($(this).css('left').replace('px', '')) > (posotion.left - num)
      const inY = parseFloat($(this).css('top').replace('px', '')) < (posotion.top + num) && parseFloat($(this).css('top').replace('px', '')) > (posotion.top - num)
      if (inX && inY) {
        count++
      }
    })
    if (count > 0) {
      return computPosition({ top: posotion.top + 50, left: posotion.left + 50 }, num); f
    } else {
      return posotion
    }
  }
  // 计算浮窗位置及避免边界碰撞方法
  const computInfoWindowPosition = (e) => {
    const windowX = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true))
    const windowY = e.originalEvent.pageY - ($('.l000_opera000_view2').offset().top)
      // const windowX = e.originalEvent.pageX - ($('#' + configObj.mainBoxId).offset().left + $('.l000_left000_view').outerWidth(true)+120)
      // const windowY = e.originalEvent.pageY - ($('.l000_opera000_view').offset().top+100)
      // console.log('windowX',windowX);
      // console.log('windowY',windowY);
    const limitX = $('.l000_opera000_view2').outerWidth(true) - $('.l000_torp000_info000_window').outerWidth(true)
    const limitY = $('.l000_opera000_view2').outerHeight(true) - $('.l000_torp000_info000_window').outerHeight(true)
    const position = {
      top: windowY,
      left: windowX,
      right: 'unset',
      bottom: 'unset'
    }
    if (windowX >= limitX) {
      position.left = 'unset'
      position.right = $('.l000_opera000_view2').outerWidth(true) - windowX + 20
    }
    if (windowY >= limitY) {
      position.top = 'unset'
      position.bottom = $('.l000_opera000_view2').outerHeight(true) - windowY + 20
    }
    return JSON.stringify(position)
  }
  // 获取拓扑数据
  this.getTorpData = () => {
    return configObj.torpData
  }
  // 设置拓扑数据
  this.setTorpData = (data) => {
    // console.log('data666', data)
    // console.log('data777', init_data)
    var all_data = data
    const isArry = Object.prototype.toString.call(data) === '[object Object]';
    const hasNode = Object.prototype.toString.call(data.nodes) === '[object Array]';
    const hasLinkes = Object.prototype.toString.call(data.links) === '[object Array]';
    if (isArry && hasNode && hasLinkes) {
      configObj.torpData = data
      $('#' + configObj.mainBoxId).empty()
      this.init()
      var init_arr = []
      // init_data.topology[0].node.forEach((j, h) => {
      //   const reg5 = new RegExp('\\.', 'g')
      //   if (j['node-id'].match(reg5)) {
      //     console.log('h123', h)
      //     init_arr.push(h)
      //   }
      // })
      data.nodes.forEach((v, w) => {        
        const elBox = $('<div>').addClass('l000_torp000_element ' + v.otherClassName).css({ 'top': v.y + 'px', 'left': v.x + 'px' }).appendTo($('.l000_opera000_view2'))
        elBox.attr('data-win', JSON.stringify({
          'machId': v.oraData['node-id'],
          'machType': v.oraData['device-family'],
          'machTypeName': v.oraData['device-type'],
          'host': v.oraData['host'],
          'buttonInfo': v.oraData['urls']
        }))
        // console.log('w123', w)
        // array.forEach(element => {

        // })
        const div = $('<div><p>' + v.name + '</p></div>').attr({ 'id': v.id, 'data-name': v.name, 'data-background-id': v.background_id }).addClass('l000_drag000_element').css({ 'background': v.background + ' #fff center no-repeat', 'background-size': '100% 100%' }).appendTo(elBox)
        // 添加连线锚点方法
        addPoint(elBox)

        if (configObj.onlyDrag) {
          changeBind(div)
        }
        if (configObj.couldEdit) {
          const closeBtn = $('<div>+</div>').addClass('l000_del000_torp').appendTo(elBox)
          // 改变clone元素的绑定事件方法
          changeBind(div)
          closeBtn.on('click', (e) => {
            if (confirm('确认删除此元素吗？')) {
              $('.l000_right000_box').hide()
              $('#l000_img000_file').val('')
              $('#img_view').css('background', '#ccc')

              elBox.remove()
              const afterDeleteNodeArr = []
              configObj.torpData.nodes.forEach((v) => {
                if (v.id !== div.prop('id')) {
                  afterDeleteNodeArr.push(v)
                }
              })
              configObj.torpData.nodes = afterDeleteNodeArr
              const afterDeletePositionArr = []
              configObj.torpData.links.forEach((v) => {
                if (v.source.indexOf(div.prop('id').split('000_')[2]) < 0 && v.target.indexOf(div.prop('id').split('000_')[2]) < 0) {
                  afterDeletePositionArr.push(v)
                }
              })
              // console.log('afterDeletePositionArr888', afterDeletePositionArr)
              configObj.torpData.links = afterDeletePositionArr
              refreshCanvas($('#' + configObj.canvasId), e, false)
            }
          })
        }
      })
      data.links.forEach((v) => {
        addDotClass(v.source)
        addDotClass(v.target)
      })
      refreshCanvas($('#' + configObj.canvasId), undefined, false)
    } else {
      alert('数据格式有误')
    }
  }

  const constructor = (conf) => {
    if (Object.prototype.toString.call(conf) === '[object Object]') {
      // 如果实例有传参，且参数是object，则执行合并配置项变量的方法
      // console.log(111111111111111111111)
      mergeObjectKey(conf, baseConfig)
    } else {
      // 如果没有参数或者参数格式不正确，则使用基本配置项
      // console.log(22222222222222222)
      mergeObjectKey(configObj, baseConfig)
    }
    this.init()
  }
  constructor(para)
}
