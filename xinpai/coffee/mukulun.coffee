import assert from 'assert'
import { XinPaiBasic } from './xinpaibasic.coffee'

class MuKuLun
	muku:'辰戌丑未'
	tiangan:"甲乙丙丁戊己庚辛壬癸"
	dizhi:"子丑寅卯辰巳午未申酉戌亥"
	# 同柱时，地支对天干的作用
	tongzhuWangshuai:
		"辰":[-1,-1,-1,-1,1,1,1,1,1,1]#√
		"戌":[-1,-1,1,1,1,1,-1,-1,-1,-1]#√
		"丑":[-1,-1,-1,-1,1,1,1,1,1,1,]#√
		"未":[-1,-1,1,1,1,1,-1,-1,-1,-1]#√
	
	# 日主生于辰戌丑未月
	RiGanYuelingWangshuai:
		"辰":[-1,-1,-1,-1,0,0,1,1,0,0]#√
		"戌":[-1,-1,0,0,0,1,-1,-1,-1,-1]#√
		"丑":[-1,-1,-1,-1,0,0,0,1,0,1]#√
		"未":[-1,-1,0,1,1,1,-1,-1,-1,-1]#√
	
	# 月令空亡，日主生于辰戌丑未年支
	RiGanNianLingWangshuai:
		"辰":[-1,-1,-1,-1,0,0,1,1,0,0]
		"戌":[-1,-1,0,0,0,1,-1,-1,-1,-1]
		"丑":[-1,-1,-1,-1,1,0,0,1,0,1]
		"未":[-1,-1,0,1,1,1,-1,-1,-1,-1]

	# 辰戌丑未年支是否为月干的根
	NianZhiYueGanWangshuai:
		"辰":["戊","庚","辛",'壬']
		"戌":["丙"]
		"丑":["己","戊","庚","辛",'癸']
		"未":["丁"]
	# 月支是辰戌丑未土，对月干的作用
	yueZhuGen:
		"辰":["戊","壬"]#√
		"戌":["丙","戊"]#√
		"丑":["己","癸"]#√
		"未":["丁",'己']
	
	constructor:()->
	
	###*
	 * 非月柱的其他柱旺衰
	 * @param  {object} tiangan 天干对象
	 * @param  {object} dizhi   地支对象
	 * @return {boolean}         是否旺
	###
	otherTongzhuWangshuai:(tiangan,dizhi)=>
		assert @muku.indexOf(dizhi.name)>=0,'地支必须是辰戌丑未中的一个'
		if @tongzhuWangshuai[dizhi.name][@tiangan.indexOf tiangan.name]>0 then true else false

	###*
	 * 月柱的同柱旺衰
	 * @param  {object} tiangan 天干对象
	 * @param  {object} dizhi   地支对象
	 * @return {boolean}         是否旺
	###
	yuezhuWangShuai:(tiangan,dizhi)=>
		assert @muku.indexOf(dizhi.name)>=0,'地支必须是辰戌丑未中的一个'
		if @yueZhuGen[dizhi.name].indexOf(tiangan.name)>=0 then true else false

	###*
	 * 日干生于辰戌丑未月的旺衰
	 * @param  {object} tiangan 天干对象
	 * @param  {object} dizhi   地支对象
	 * @return {boolean}         是否旺
	###	
	RiGanWangshuaiYuYueling:(tiangan,dizhi)=>
		assert @muku.indexOf(dizhi.name)>=0,'地支必须是辰戌丑未中的一个'
		@RiGanYuelingWangshuai[dizhi.name][@tiangan.indexOf tiangan.name]
	
	###*
	 * 日干生于辰戌丑未年支的旺衰，当前与月令一样
	 * @param  {object} tiangan 天干对象
	 * @param  {object} dizhi   地支对象
	 * @return {boolean}         是否旺
	###	
	RiGanWangshuaiYuNianling:(tiangan,dizhi)=>
		assert @muku.indexOf(dizhi.name)>=0,'地支必须是辰戌丑未中的一个'
		if @RiGanNianLingWangshuai[dizhi.name][@tiangan.indexOf tiangan.name]>0 then true else false

	###*
	 * 辰戌丑未年支，是否是月干的根
	 * @param  {object} tiangan 天干对象
	 * @param  {object} dizhi   地支对象
	 * @return {boolean}         是否旺
	###	
	YueGanWangshuaiYuNianZhi:(tiangan,dizhi)=>
		assert @muku.indexOf(dizhi.name)>=0,'地支必须是辰戌丑未中的一个'
		if @NianZhiYueGanWangshuai[dizhi.name].indexOf(tiangan.name)>=0 then true else false


# a=new MuKuLun()
# console.log a.RiGanWangshuaiYuYueling({name:'庚'},{name:'戌'})
exports.MuKuLun=MuKuLun