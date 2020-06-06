
class XuShiShen
	###*
	 * 构造函数
	 * @param  {object} @bazi         八字对象
	 * @param  {string} @tianganDizhi 年的天干地支，例如“丁卯”
	###
	constructor:(@bazi,@tianganDizhi)->
		@shishen=@getShishen()
		@xushen=@getXushen()

	###*
	 * [getShishen description]
	 * @return {[type]} [description]
	###
	getShishen:()=>
		result={}
		if @bazi.str.indexOf(@tianganDizhi[0])>=0 then result.tiangan=@tianganDizhi[0]
		if @bazi.str.indexOf(@tianganDizhi[1])>=0 then result.dizhi=@tianganDizhi[1]
		result
	
	getXushen:()=>
		result={}
		if @bazi.str.indexOf(@tianganDizhi[0])==-1 then result.tiangan=@tianganDizhi[0]
		if @bazi.str.indexOf(@tianganDizhi[1])==-1 then result.dizhi=@tianganDizhi[1]
		result
							
exports.XuShiShen=XuShiShen