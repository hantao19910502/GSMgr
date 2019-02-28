<?php

/***************************************************************************
 *
 * Copyright (c) 2010 babeltime.com, Inc. All Rights Reserved
 * $Id: Game.cfg.php 62291 2013-08-30 14:11:01Z wuqilin $
 *
 **************************************************************************/

/**
 * @file $HeadURL: svn://192.168.1.80:3698/C/tags/card/rpcfw/rpcfw_1-0-0-3/conf/gsc/game001/Game.cfg.php $
 * @author $Author: wuqilin $(hoping@babeltime.com)
 * @date $Date: 2013-08-30 22:11:01 +0800 (五, 2013-08-30) $
 * @version $Revision: 62291 $
 * @brief
 *
 **/
class GameConf
{

	/**
	 * 开服年月日
	 * @var string
	 */
const SERVER_OPEN_YMD = '20171221';

	/**
	 * 开服时分秒
	 * @var string
	 */
const SERVER_OPEN_TIME = '173400';

	/**
	 * boss 错峰时间偏移
	 * @var int
	 */
const BOSS_OFFSET = 1800;

}

/**
 * 如果需要修改竞技场持续天数，
 * 应该也同时修改竞技场开始日期为当前日期
 *
 * @author idyll
 *
 */
class ArenaDateConf
{
	//持续天数
	const LAST_DAYS = 1;

	//锁定开始时间
	const LOCK_START_TIME = "22:00:00";

	//锁定结束时间
	const LOCK_END_TIME = "22:50:00";
}
/* vim: set ts=4 sw=4 sts=4 tw=100 noet: */
