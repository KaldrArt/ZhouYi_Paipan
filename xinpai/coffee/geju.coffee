
import {Bazi} from '../basic/bazi.coffee'
import {XinPaiBasic} from './xinpaibasic.coffee'
import {MuKuLun} from './mukulun.coffee'

class XinPaiGeju
	# 格局类型
	gejuType:
		wangshuai:false # 旺true，弱false
		cong:true # 从true，身false
	# 时干、月干是否有力
	gejuYouli:
		ShiGan:-1
		YueGan:-1
		yueling:1
	# 年支、日支、月干、时干对日主的扶、制作用
	# 0为不旺不弱
	# 1为扶
	# -1为制
	gejuRelation:
		NianZhi:0
		RiZhi:0
		YueGan:0
		ShiGan:0

	constructor:(@bazi)->
		@MuKuLun=new MuKuLun()
		@XinPaiBasic=new XinPaiBasic()
		@yueLingWangShuai()
		@cong()
	###*
	 * 是否从
	 * @return {boolean} true从，false身
	###
	cong:()=>
		@RiZhiDuiRizhu()
		@YueGanRelation()
		@YueGanPower()
		@ShiGanRelation()
		@ShiGanPower()
		# 如果是月令两次受制，并且日支、年支对日主作用一致，那么格局已经断过了，否则
		if not @geju
			# 旺
			if @gejuType.wangshuai
				if @gejuRelation.RiZhi<0 or (@gejuRelation.YueGan<0 and @gejuYouli.YueGan>0) or (@gejuRelation.ShiGan<0 and @gejuYouli.ShiGan>0) then @gejuType.cong=false
			# 弱
			else
				if @gejuRelation.RiZhi>0 or (@gejuRelation.YueGan>0 and @gejuYouli.YueGan>0) or (@gejuRelation.ShiGan>0 and @gejuYouli.ShiGan>0) then @gejuType.cong=false
			if @gejuType.wangshuai
				if @gejuType.cong then @geju='从旺' else @geju='身旺'
			else
				if @gejuType.cong then @geju='从弱' else @geju='身弱'
	###*
	 * 月干与日主之间的关系
	###
	YueGanRelation:()=>
		@gejuRelation.YueGan= if @XinPaiBasic.tianganWangshuai @bazi.RiGan,@bazi.YueGan then 1 else -1
	
	###*
	 * 月干是否有力
	###
	YueGanPower:()=>
		if @NianZhiDuiYueGanWang() then @gejuYouli.YueGan=1
		if @NianGanDuiYueGanWang() then @gejuYouli.YueGan=1
		if @YueZhiDuiYueGanWang() then @gejuYouli.YueGan=1
	
	NianZhiDuiYueGanWang:()=>
		if '辰戌丑未'.indexOf(@bazi.NianZhi.name)>=0
			if @MuKuLun.YueGanWangshuaiYuNianZhi @bazi.YueGan,@bazi.NianZhi then true else false
		else
			if @XinPaiBasic.wangshuai @bazi.YueGan,@bazi.NianZhi then true else false

	NianGanDuiYueGanWang:()=>
		if @XinPaiBasic.tianganWangshuai @bazi.YueGan,@bazi.NianGan then true else false


	YueZhiDuiYueGanWang:()=>
		result=false
		if '辰戌丑未'.indexOf(@bazi.YueZhi.name)>=0
			if @MuKuLun.otherTongzhuWangshuai @bazi.YueGan,@bazi.YueZhi then result=true else result=false
		else
			if @XinPaiBasic.wangshuai @bazi.YueGan,@bazi.YueZhi then result=true else result=false
		if @bazi.kongwang.indexOf(@bazi.YueZhi.name)>=0 then result=!result
		result
	###*
	 * 时干与日主之间的关系
	###
	ShiGanRelation:()=>
		@gejuRelation.ShiGan=if @XinPaiBasic.tianganWangshuai @bazi.RiGan,@bazi.ShiGan then 1 else -1
	
	###*
	 * 时干是否有力
	###
	ShiGanPower:()=>
		if '辰戌丑未'.indexOf(@bazi.ShiZhi.name)>=0
			if @MuKuLun.otherTongzhuWangshuai @bazi.ShiGan,@bazi.ShiZhi then @gejuYouli.ShiGan=1 else @gejuYouli.ShiGan=-1
		else
			if @XinPaiBasic.wangshuai @bazi.ShiGan,@bazi.ShiZhi then @gejuYouli.ShiGan=1 else @gejuYouli.ShiGan=-1
		if @bazi.kongwang.indexOf(@bazi.ShiZhi.name)>=0 then @gejuYouli.ShiGan=-1*@gejuYouli.ShiGan
	###*
	 * 月令是否空亡
	 * @return {boolean} 是否空亡
	###
	yueLingKongWang:()=>
		if @bazi.kongwang.indexOf(@bazi.YueZhi.name)>=0 then yes else no

	###*
	 * 月令是否两次受制
	 * @return {boolean} 是否两次受制
	###
	yueLingLiangCiShouZhi:()=>
		score=0
		if @XinPaiBasic.dizhiBeiZhi @bazi.YueZhi,@bazi.RiZhi 
			score+=1
			#console.log "月令被日支制"
		if @XinPaiBasic.dizhiBeiZhi @bazi.YueZhi,@bazi.NianZhi
			score+=1
			#console.log "月令被年支制"
		score
	
	###*
	 * 日支是否两次受制
	 * @return {boolean} 日支是否两次受制
	###
	RiZhiLiangCiShouZhi:()=>
		score=0
		if @XinPaiBasic.dizhiBeiZhi @bazi.RiZhi,@bazi.ShiZhi then score+=1
		if @XinPaiBasic.dizhiBeiZhi @bazi.RiZhi,@bazi.YueZhi then score+=1
		if score==2 then true else false
	###*
	 * 日主生于月令的旺衰情况
	 * @return {boolean} 旺true弱false 
	###
	yueLingWangShuai:()=>
		# 月令空亡
		if @yueLingKongWang()
			#console.log "月令空亡，看年支旺衰"
			if @NianZhiWangShuai()
				#console.log "旺"
				@gejuType.wangshuai=true
			else
				#console.log "弱"
				@gejuType.wangshuai=false
		# 月令不空亡
		else
			if @yuelingWuLi()
				#console.log '月令无力'
				if @gejuRelation.RiZhi>0
					#console.log "旺"
					@gejuType.wangshuai=true
					if @XinPaiBasic.rizhuYuelingWangshuai @bazi.RiGan,@bazi.YueZhi < 0
						#console.log "月令始终有点力制日主"
						@geju='身旺'
						@gejuType.cong=false
				else
					#console.log "弱"
					@gejuType.wangshuai=false
					if @XinPaiBasic.rizhuYuelingWangshuai @bazi.RiGan,@bazi.YueZhi > 0
						#console.log "月令始终有点力生日主"
						@geju='身弱'
						@gejuType.cong=false

			# 月令有力
			else
				rizhuWangshuaiYuYueling=@XinPaiBasic.rizhuYuelingWangshuai @bazi.RiGan,@bazi.YueZhi
				# 日主旺与月令
				if rizhuWangshuaiYuYueling==1
					#console.log '旺'
					@gejuType.wangshuai=true
				# 日主弱与月令
				else if rizhuWangshuaiYuYueling==-1
					#console.log '弱'
					@gejuType.wangshuai=false
				# 日主不旺不弱
				else if rizhuWangshuaiYuYueling==0
					#console.log "日主不旺不弱，需要看月干"
					# 月干对日主旺
					if @YueGanDuiRizhuWang()
						#console.log "旺"
						@gejuType.wangshuai=true
					# 月干对日主弱
					else
						#console.log '弱'
						@gejuType.wangshuai=false
	###*
	 * 月干对日主的旺衰作用
	 * @return {boolean} true旺，false弱
	###
	YueGanDuiRizhuWang:()=>
		if @XinPaiBasic.tianganWangshuai @bazi.RiGan,@bazi.YueGan then true else false

	###*
	 * 判断月令是否无力
	 * @return {boolean} 1无力，0有力
	###
	yuelingWuLi:()=>
		# 月令两次受制
		if @yueLingLiangCiShouZhi()==2 
			#console.log "月令两次受制"
			# 日支两次受制
			if @RiZhiLiangCiShouZhi()
				console.log "日支两次受制，月令有力"
				false
			# 日支受制1次或者更少
			else
				# 年支和日支对日主的作用一致
				if @NianZhiDuiRizhu() == @RiZhiDuiRizhu()
					#console.log '年支和日支对日主的作用一致'
					@gejuYouli.yueling=-1
					true
				# 年支和日支对日主作用不一致
				else
					false
		# 月令受制1次或者没有受制
		else
			false
	
	###*
	 * 年支对日主的作用
	 * @return {number} 1，帮扶，-1 抑制
	###
	NianZhiDuiRizhu:()=>
		if @gejuRelation.NianZhi==0
			if '辰戌丑未'.indexOf(@bazi.NianZhi.name)>=0
				if @MuKuLun.otherTongzhuWangshuai @bazi.RiGan,@bazi.NianZhi then @gejuRelation.NianZhi=1 else @gejuRelation.NianZhi=-1
			else
				if @XinPaiBasic.wangshuai @bazi.RiGan,@bazi.NianZhi then @gejuRelation.NianZhi=1 else @gejuRelation.NianZhi=-1
		@gejuRelation.NianZhi
	
	###*
	 * 日支对日主的作用
	 * @return {number} 1，帮扶，-1，抑制
	###
	RiZhiDuiRizhu:()=>
		if @gejuRelation.RiZhi==0
			if '辰戌丑未'.indexOf(@bazi.RiZhi.name)>=0
				if @MuKuLun.otherTongzhuWangshuai @bazi.RiGan,@bazi.RiZhi then @gejuRelation.RiZhi=1 else @gejuRelation.RiZhi=-1
			else
				if @XinPaiBasic.wangshuai @bazi.RiGan,@bazi.RiZhi then @gejuRelation.RiZhi=1 else @gejuRelation.RiZhi=-1
		@gejuRelation.RiZhi

	###*
	 * 日主生于年支时的旺衰
	 * @return {boolean} 1旺，0弱
	###
	NianZhiWangShuai:()=>
		if @XinPaiBasic.rizhuNianLingWangshuai @bazi.RiGan,@bazi.NianZhi
			true
		else
			false
	
exports.XinPaiGeju=XinPaiGeju