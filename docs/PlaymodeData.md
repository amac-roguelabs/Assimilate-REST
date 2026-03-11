# PlaymodeData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**audio** | **str** | Audio settings | [optional]
**fps** | **float** | Playback framerate | [optional]
**target_fps** | **float** | Target framerate of the current timeline/construct (configured FPS, independent of playback speed) | [optional] [proposed]
**frame** | **int** | Current frame position | [optional]
**length** | **int** | Length of the media in the Player in frames | [optional]
**loop** | **str** | Loop mode | [optional]
**mark_in** | **int** | View range in-point | [optional]
**mark_out** | **int** | View range out-point | [optional]
**mode** | **str** | Playback mode (PAUSE, PLAY_FRW, PLAY_REV, RECORD, STOP, JOG_FRW, JOG_REV, SHUTTLE_FRW, SHUTTLE_REV) | [optional]
**range** | **bool** | View range is active / not | [optional]
**speed** | **int** | Playback multiplier | [optional]
**tc** | **str** | Current timecode | [optional]
**src_tc** | **str** | Source timecode of the current shot at the current frame position | [optional] [proposed]
**timeline** | **str** | Name of the construct being played | [optional]
**duration** | **int** | Total duration of the current construct/timeline in frames | [optional] [proposed]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

